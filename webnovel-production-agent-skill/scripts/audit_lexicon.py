#!/usr/bin/env python3
"""Validate lexicon files and optionally audit a Korean manuscript."""
from __future__ import annotations

import argparse
import json
import re
import sys
from collections import Counter
from pathlib import Path
from typing import Any

try:
    import jsonschema
except ImportError as exc:  # pragma: no cover
    raise SystemExit("jsonschema is required: pip install jsonschema") from exc

ROOT = Path(__file__).resolve().parents[1]


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def add_issue(issues: list[dict[str, Any]], severity: str, code: str, path: str, message: str, **extra: Any) -> None:
    issue: dict[str, Any] = {"severity": severity, "code": code, "path": path, "message": message}
    issue.update(extra)
    issues.append(issue)


def count_matches(text: str, surface: str, match_type: str) -> int:
    if match_type == "regex":
        try:
            return len(re.findall(surface, text))
        except re.error:
            return -1
    if match_type == "exact":
        return sum(1 for token in re.findall(r"\S+", text) if token.strip(".,!?\"'“”‘’()[]{}") == surface)
    if match_type == "document_metric":
        return 0
    return text.count(surface)


def count_matches(text: str, surface: str, match_type: str) -> int:
    """Count phrase matches with ASCII-safe punctuation stripping for exact mode."""
    if match_type == "regex":
        try:
            return len(re.findall(surface, text))
        except re.error:
            return -1
    if match_type == "exact":
        return sum(1 for token in re.findall(r"\S+", text) if token.strip(".,!?\"'()[]{}") == surface)
    if match_type == "document_metric":
        return 0
    return text.count(surface)


def load_lexicons(paths: list[Path], schema_path: Path, issues: list[dict[str, Any]]) -> list[tuple[Path, dict[str, Any]]]:
    schema = load_json(schema_path)
    validator = jsonschema.Draft202012Validator(schema)
    docs: list[tuple[Path, dict[str, Any]]] = []
    for path in paths:
        try:
            doc = load_json(path)
        except json.JSONDecodeError as exc:
            add_issue(issues, "error", "LEXICON_JSON_PARSE", str(path), str(exc))
            continue
        errors = sorted(validator.iter_errors(doc), key=lambda err: list(err.path))
        for error in errors:
            location = ".".join(str(part) for part in error.path) or "$"
            add_issue(issues, "error", "LEXICON_SCHEMA", f"{path}:{location}", error.message)
        if not errors:
            docs.append((path, doc))
    return docs


def audit_structure(docs: list[tuple[Path, dict[str, Any]]], issues: list[dict[str, Any]]) -> None:
    ids: Counter[str] = Counter()
    surfaces: dict[tuple[str, str], list[str]] = {}
    for path, doc in docs:
        for entry in doc.get("entries", []):
            entry_id = entry["id"]
            surface = entry["surface"]
            ids[entry_id] += 1
            surfaces.setdefault((surface, entry["kind"]), []).append(f"{path.name}:{entry_id}")
            if entry.get("severity") == "S1" and not entry.get("replacement"):
                add_issue(issues, "warning", "S1_REPLACEMENT_MISSING", f"{path}:{entry_id}", "S1 entry should describe a replacement policy.")
            if entry.get("kind") in {"ai_tell_phrase", "prohibited_phrase"} and not entry.get("threshold"):
                add_issue(issues, "warning", "THRESHOLD_MISSING", f"{path}:{entry_id}", "Phrase audit entry should define a threshold.")

    for entry_id, count in ids.items():
        if count > 1:
            add_issue(issues, "error", "DUPLICATE_ENTRY_ID", entry_id, f"Entry id appears {count} times.")
    for (surface, _kind), owners in surfaces.items():
        if len(owners) > 1:
            add_issue(issues, "warning", "DUPLICATE_SURFACE", surface, "Surface appears in multiple entries.", owners=owners)


def audit_manuscript(text: str, docs: list[tuple[Path, dict[str, Any]]], issues: list[dict[str, Any]]) -> dict[str, Any]:
    hits: list[dict[str, Any]] = []
    for path, doc in docs:
        for entry in doc.get("entries", []):
            if entry.get("kind") not in {"ai_tell_phrase", "prohibited_phrase"}:
                continue
            count = count_matches(text, entry["surface"], entry.get("match_type", "substring"))
            if count < 0:
                add_issue(issues, "error", "REGEX_INVALID", f"{path}:{entry['id']}", "Invalid regex pattern.")
                continue
            threshold = entry.get("threshold", 1)
            if count >= threshold:
                hit = {
                    "id": entry["id"],
                    "surface": entry["surface"],
                    "kind": entry["kind"],
                    "category": entry.get("category"),
                    "severity": entry.get("severity", "info"),
                    "count": count,
                    "threshold": threshold,
                    "source": str(path.relative_to(ROOT)),
                    "replacement": entry.get("replacement", "")
                }
                hits.append(hit)
                issue_severity = "error" if entry.get("severity") == "S1" else "warning"
                add_issue(
                    issues,
                    issue_severity,
                    "MANUSCRIPT_PHRASE_HIT",
                    f"{path}:{entry['id']}",
                    f"'{entry['surface']}' matched {count} time(s), threshold {threshold}.",
                    hit=hit,
                )
    return {
        "checked_characters": len(text),
        "hit_count": len(hits),
        "hits": hits,
    }


def default_lexicon_paths() -> list[Path]:
    return sorted((ROOT / "lexicons").glob("*.json"))


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("lexicons", nargs="*", type=Path, help="Lexicon JSON files. Defaults to lexicons/*.json.")
    parser.add_argument("--schema", type=Path, default=ROOT / "schemas" / "lexicon.schema.json")
    parser.add_argument("--manuscript", type=Path, help="Optional manuscript text to audit.")
    parser.add_argument("--allow-hits", action="store_true", help="Return success even when manuscript phrase hits are found.")
    args = parser.parse_args()

    paths = [path.resolve() for path in args.lexicons] if args.lexicons else default_lexicon_paths()
    issues: list[dict[str, Any]] = []
    if not paths:
        add_issue(issues, "error", "NO_LEXICONS", "lexicons", "No lexicon files found.")
    docs = load_lexicons(paths, args.schema, issues) if paths else []
    audit_structure(docs, issues)

    manuscript_report = None
    if args.manuscript:
        text = args.manuscript.read_text(encoding="utf-8")
        manuscript_report = audit_manuscript(text, docs, issues)

    errors = [issue for issue in issues if issue["severity"] == "error"]
    warnings = [issue for issue in issues if issue["severity"] == "warning"]
    phrase_errors = [issue for issue in errors if issue["code"] == "MANUSCRIPT_PHRASE_HIT"]
    effective_errors = [issue for issue in errors if not (args.allow_hits and issue["code"] == "MANUSCRIPT_PHRASE_HIT")]
    result = {
        "status": "FAIL" if effective_errors else ("WARN" if warnings or phrase_errors else "PASS"),
        "lexicon_count": len(docs),
        "entry_count": sum(len(doc.get("entries", [])) for _, doc in docs),
        "manuscript": manuscript_report,
        "errors": errors,
        "warnings": warnings,
        "metrics": {
            "error_count": len(errors),
            "warning_count": len(warnings),
        },
    }
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 1 if effective_errors else 0


if __name__ == "__main__":
    sys.exit(main())

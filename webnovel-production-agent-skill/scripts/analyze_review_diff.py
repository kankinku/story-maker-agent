#!/usr/bin/env python3
"""Create explicit manuscript review diffs and aggregate repeated scoped patterns."""
from __future__ import annotations

import argparse
import difflib
import hashlib
import json
import sys
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator

ROOT = Path(__file__).resolve().parents[1]
POLICY = json.loads((ROOT / "config" / "context_compounding_policy.json").read_text(encoding="utf-8"))
ALLOWED = set(POLICY["outer_loop"]["classifications"])
REVIEW_DIFF_SCHEMA = json.loads((ROOT / "schemas" / "review_diff.schema.json").read_text(encoding="utf-8"))


def sha256(text: str) -> str:
    return "sha256:" + hashlib.sha256(text.encode("utf-8")).hexdigest()


def parse_hypothesis(value: str) -> dict[str, Any]:
    parts = value.split("|", 3)
    if len(parts) != 4:
        raise ValueError("Hypothesis must be target|confidence|cause|evidence")
    target, confidence, cause, evidence = parts
    if target not in {"retrieval", "state", "prompt", "validator", "policy", "human_judgment"}:
        raise ValueError(f"Unsupported hypothesis target: {target}")
    return {"cause": cause, "target": target, "evidence": evidence, "confidence": float(confidence)}


def create(args: argparse.Namespace) -> dict[str, Any]:
    if not args.draft.exists() or not args.final.exists() or args.draft.resolve() == args.final.resolve():
        return {"status": "FAIL", "errors": [{"code": "REVIEW_PAIR_MISSING", "message": "Distinct draft and final files are required."}]}
    invalid = sorted(set(args.classification) - ALLOWED)
    if invalid:
        return {"status": "FAIL", "errors": [{"code": "SCHEMA", "message": f"Unsupported classifications: {invalid}"}]}
    if len(args.hypothesis) < 3:
        return {"status": "FAIL", "errors": [{"code": "CAUSES_TOO_FEW", "message": "At least three root-cause hypotheses are required."}]}
    draft = args.draft.read_text(encoding="utf-8")
    final = args.final.read_text(encoding="utf-8")
    draft_lines, final_lines = draft.splitlines(), final.splitlines()
    matcher = difflib.SequenceMatcher(None, draft, final)
    added = removed = 0
    for line in difflib.ndiff(draft_lines, final_lines):
        added += line.startswith("+ ")
        removed += line.startswith("- ")
    reviewed_at = args.reviewed_at or datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")
    document = {
        "schema_version": "1.0.0", "diff_id": args.diff_id, "review_id": args.review_id, "scope": args.scope,
        "draft_path": str(args.draft), "final_path": str(args.final), "draft_hash": sha256(draft), "final_hash": sha256(final),
        "similarity_ratio": round(matcher.ratio(), 6), "added_lines": added, "removed_lines": removed,
        "classifications": args.classification, "root_cause_hypotheses": [parse_hypothesis(value) for value in args.hypothesis],
        "completed": True, "reviewed_at": reviewed_at,
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(document, ensure_ascii=False, indent=2), encoding="utf-8")
    return {"status": "PASS", "errors": [], "artifact": str(args.output), "metrics": {"similarity_ratio": document["similarity_ratio"], "added_lines": added, "removed_lines": removed}}


def aggregate(args: argparse.Namespace) -> dict[str, Any]:
    documents = []
    for path in args.input_dir.glob("*.json"):
        try:
            document = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            continue
        if not list(Draft202012Validator(REVIEW_DIFF_SCHEMA).iter_errors(document)) and document.get("completed") is True and document.get("reviewed_at"):
            documents.append(document)
    window = POLICY["outer_loop"]["review_window"]
    threshold = POLICY["outer_loop"]["minimum_same_scope_occurrences"]
    maximum = POLICY["outer_loop"]["maximum_proposals_per_run"]
    unique_reviews: dict[str, dict[str, Any]] = {}
    for item in sorted(documents, key=lambda value: value["reviewed_at"], reverse=True):
        unique_reviews.setdefault(item["review_id"], item)
    recent = list(unique_reviews.values())[:window]
    grouped: dict[tuple[str, str], list[str]] = defaultdict(list)
    for item in recent:
        for classification in item.get("classifications", []):
            grouped[(item["scope"], classification)].append(item["review_id"])
    candidates = [
        {"scope": scope, "classification": classification, "count": len(review_ids), "review_ids": review_ids}
        for (scope, classification), review_ids in grouped.items() if len(review_ids) >= threshold
    ]
    candidates.sort(key=lambda item: (-item["count"], item["scope"], item["classification"]))
    candidates = candidates[:maximum]
    output = {"status": "PASS", "errors": [], "metrics": {"completed_reviews_considered": len(recent), "raw_candidate_count": len(grouped), "promotable_candidate_count": len(candidates)}, "candidates": candidates}
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(json.dumps(output, ensure_ascii=False, indent=2), encoding="utf-8")
    return output


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)
    new = sub.add_parser("create")
    new.add_argument("--draft", type=Path, required=True); new.add_argument("--final", type=Path, required=True); new.add_argument("--output", type=Path, required=True)
    new.add_argument("--diff-id", required=True); new.add_argument("--review-id", required=True); new.add_argument("--scope", required=True); new.add_argument("--reviewed-at")
    new.add_argument("--classification", action="append", required=True); new.add_argument("--hypothesis", action="append", required=True)
    agg = sub.add_parser("aggregate"); agg.add_argument("--input-dir", type=Path, required=True); agg.add_argument("--output", type=Path)
    args = parser.parse_args()
    try:
        output = create(args) if args.command == "create" else aggregate(args)
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        output = {"status": "FAIL", "errors": [{"code": "INPUT", "message": str(exc)}]}
    print(json.dumps(output, ensure_ascii=False, indent=2))
    return 0 if output["status"] == "PASS" else 1


if __name__ == "__main__":
    sys.exit(main())

#!/usr/bin/env python3
"""Audit a hash-bound source/rewrite fidelity contract deterministically."""
from __future__ import annotations

import argparse
import hashlib
import json
import sys
from pathlib import Path
from typing import Any

try:
    import jsonschema
except ImportError as exc:  # pragma: no cover
    raise SystemExit("jsonschema is required: pip install jsonschema") from exc

ROOT = Path(__file__).resolve().parents[1]


def load(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8-sig"))


def sha256(path: Path) -> str:
    return "sha256:" + hashlib.sha256(path.read_bytes()).hexdigest()


def add(issues: list[dict[str, str]], code: str, path: str, message: str) -> None:
    issues.append({"code": code, "path": path, "message": message})


def verify_bound_file(
    contract_path: Path,
    binding: dict[str, str],
    label: str,
    issues: list[dict[str, str]],
) -> Path | None:
    path = (contract_path.parent / binding["path"]).resolve()
    if not path.is_file():
        add(issues, f"REWRITE_{label.upper()}_FILE_MISSING", f"{label}.path", f"File not found: {path}")
        return None
    actual = sha256(path)
    if actual != binding["sha256"]:
        add(
            issues,
            f"REWRITE_{label.upper()}_HASH_MISMATCH",
            f"{label}.sha256",
            f"Expected {binding['sha256']}, found {actual}.",
        )
    return path


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("contract", type=Path)
    parser.add_argument("--schema", type=Path, default=ROOT / "schemas" / "rewrite_fidelity_contract.schema.json")
    args = parser.parse_args()

    contract_path = args.contract.resolve()
    document = load(contract_path)
    schema_errors = sorted(
        jsonschema.Draft202012Validator(load(args.schema)).iter_errors(document),
        key=lambda error: tuple(str(part) for part in error.path),
    )
    if schema_errors:
        errors = [
            {
                "code": "SCHEMA",
                "path": ".".join(str(part) for part in error.absolute_path) or "$",
                "message": error.message,
            }
            for error in schema_errors
        ]
        print(json.dumps({"status": "FAIL", "errors": errors, "metrics": {}}, ensure_ascii=False, indent=2))
        return 1

    issues: list[dict[str, str]] = []
    source_path = verify_bound_file(contract_path, document["source"], "source", issues)
    rewrite_path = verify_bound_file(contract_path, document["rewrite"], "output", issues)
    source_text = source_path.read_text(encoding="utf-8-sig") if source_path else ""
    rewrite_text = rewrite_path.read_text(encoding="utf-8-sig") if rewrite_path else ""

    source_events = document["source_events"]
    rewrite_events = document["rewrite_events"]
    source_ids = [event["event_id"] for event in source_events]
    rewrite_ids = [event["event_id"] for event in rewrite_events]
    if len(source_ids) != len(set(source_ids)):
        add(issues, "REWRITE_EVENT_ID_DUPLICATE", "source_events", "Source event IDs must be unique.")
    if len(rewrite_ids) != len(set(rewrite_ids)):
        add(issues, "REWRITE_EVENT_ID_DUPLICATE", "rewrite_events", "Rewrite event IDs must be unique.")

    source_by_id = {event["event_id"]: event for event in source_events}
    mapped_source_ids = {
        event["source_event_id"]
        for event in rewrite_events
        if event.get("source_event_id") in source_by_id
    }
    for event in source_events:
        if event["required"] and event["event_id"] not in mapped_source_ids:
            add(issues, "REWRITE_EVENT_MISSING", f"source_events.{event['event_id']}", "Required source event is not mapped in the rewrite.")

    for event in rewrite_events:
        source_event_id = event.get("source_event_id")
        if source_event_id not in source_by_id and not event["approved_invention"]:
            add(issues, "REWRITE_EVENT_INVENTED", f"rewrite_events.{event['event_id']}", "Rewrite event has no source mapping or approval.")

    ordered_pairs = sorted(
        (
            (event["order"], source_by_id[event["source_event_id"]]["order"])
            for event in rewrite_events
            if event.get("source_event_id") in source_by_id
        ),
        key=lambda pair: pair[0],
    )
    source_order = [pair[1] for pair in ordered_pairs]
    if source_order != sorted(source_order):
        add(issues, "REWRITE_EVENT_REORDERED", "rewrite_events", "Mapped source events changed relative order.")

    rewrite_entities = set(document["rewrite_entities"])
    allowed_renames = document["allowed_entity_renames"]
    for entity in document["preserve_entities"]:
        expected = allowed_renames.get(entity, entity)
        if entity not in source_text:
            add(issues, "REWRITE_SOURCE_EVIDENCE_INVALID", f"preserve_entities.{entity}", "Preserved entity is absent from the bound source text.")
        if expected not in rewrite_entities or expected not in rewrite_text:
            add(issues, "REWRITE_ENTITY_DRIFT", f"preserve_entities.{entity}", f"Expected entity {expected!r} is absent from rewrite evidence.")

    rewrite_quotes = set(document["rewrite_quotes"])
    for quote in document["protected_quotes"]:
        if quote not in source_text:
            add(issues, "REWRITE_SOURCE_EVIDENCE_INVALID", "protected_quotes", f"Protected quote is absent from bound source text: {quote!r}")
        if quote not in rewrite_quotes or quote not in rewrite_text:
            add(issues, "REWRITE_QUOTE_DRIFT", "protected_quotes", f"Protected quote is absent or changed: {quote!r}")

    result = {
        "status": "FAIL" if issues else "PASS",
        "errors": issues,
        "metrics": {
            "source_event_count": len(source_events),
            "rewrite_event_count": len(rewrite_events),
            "mapped_event_count": len(mapped_source_ids),
            "preserved_entity_count": len(document["preserve_entities"]),
            "protected_quote_count": len(document["protected_quotes"]),
        },
    }
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 1 if issues else 0


if __name__ == "__main__":
    raise SystemExit(main())

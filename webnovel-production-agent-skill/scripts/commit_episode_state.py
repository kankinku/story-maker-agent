#!/usr/bin/env python3
"""Apply an approved episode delta to structured state, with dry-run support."""
from __future__ import annotations

import argparse
import json
import sys
from copy import deepcopy
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator

ROOT = Path(__file__).resolve().parents[1]


def load(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8-sig"))


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--character-state", type=Path, required=True)
    parser.add_argument("--relationship-state", type=Path, required=True)
    parser.add_argument("--delta", type=Path, required=True)
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    try:
        character_doc, relationship_doc, delta = load(args.character_state), load(args.relationship_state), load(args.delta)
    except (OSError, json.JSONDecodeError) as exc:
        print(json.dumps({"status": "FAIL", "errors": [{"code": "INPUT", "message": str(exc)}]}, ensure_ascii=False, indent=2)); return 1
    schema_pairs = [
        (character_doc, "character_state.schema.json"),
        (relationship_doc, "relationship_state.schema.json"),
        (delta, "episode_memory_delta.schema.json"),
    ]
    schema_errors = []
    for document, schema_name in schema_pairs:
        schema = load(ROOT / "schemas" / schema_name)
        schema_errors.extend(error.message for error in Draft202012Validator(schema).iter_errors(document))
    if schema_errors:
        print(json.dumps({"status": "FAIL", "errors": [{"code": "SCHEMA", "message": message} for message in schema_errors]}, ensure_ascii=False, indent=2)); return 1
    errors = []
    approval = delta.get("human_approval", {})
    if delta.get("continuity_check", {}).get("status") != "pass" or approval.get("status") != "approved" or not approval.get("approval_id"):
        errors.append({"code": "CANON_DELTA_UNAPPROVED", "message": "Continuity PASS and explicit human approval are required."})
    if character_doc.get("state_version") != delta.get("base_state_version") or relationship_doc.get("state_version") != delta.get("base_state_version"):
        errors.append({"code": "CHARACTER_STATE_DRIFT", "message": "Delta base version does not match both state documents."})
    if any(change.get("target_type") == "canon_decision" for change in delta.get("changes", [])):
        errors.append({"code": "CANON_TARGET_UNSUPPORTED", "message": "Canon decisions require a separately approved Story Bible change and cannot be committed to character or relationship state."})
    characters = {item["character_id"]: item for item in character_doc.get("characters", [])}
    relationships = {item["relationship_id"]: item for item in relationship_doc.get("relationships", [])}
    next_characters, next_relationships = deepcopy(character_doc), deepcopy(relationship_doc)
    next_character_index = {item["character_id"]: item for item in next_characters.get("characters", [])}
    next_relationship_index = {item["relationship_id"]: item for item in next_relationships.get("relationships", [])}
    for change in delta.get("changes", []):
        index = characters if change["target_type"] == "character" else relationships if change["target_type"] == "relationship" else None
        next_index = next_character_index if change["target_type"] == "character" else next_relationship_index if change["target_type"] == "relationship" else None
        if index is None:
            continue
        target = index.get(change["target_id"])
        if target is None or target.get(change["field"]) != change["before"]:
            errors.append({"code": "CHARACTER_STATE_DRIFT", "message": f"Before value mismatch for {change['target_id']}.{change['field']}."})
        else:
            next_index[change["target_id"]][change["field"]] = change["after"]
            next_index[change["target_id"]]["last_evidence"] = {"episode": delta["episode_number"], "source_id": change["source_id"]}
    if errors:
        print(json.dumps({"status": "FAIL", "errors": errors}, ensure_ascii=False, indent=2)); return 1
    for document in (next_characters, next_relationships):
        document["state_version"] = delta["target_state_version"]
        document["as_of_episode"] = delta["episode_number"]
    if not args.dry_run:
        args.character_state.write_text(json.dumps(next_characters, ensure_ascii=False, indent=2), encoding="utf-8")
        args.relationship_state.write_text(json.dumps(next_relationships, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps({"status": "PASS", "errors": [], "dry_run": args.dry_run, "target_state_version": delta["target_state_version"], "change_count": len(delta.get("changes", []))}, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())

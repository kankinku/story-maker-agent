#!/usr/bin/env python3
"""Validate context-compounding contracts and deterministic workflow gates."""
from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator, FormatChecker

ROOT = Path(__file__).resolve().parents[1]
SCHEMAS = {
    "context_plan": "context_plan.schema.json",
    "evidence_pack": "evidence_pack.schema.json",
    "character_state": "character_state.schema.json",
    "relationship_state": "relationship_state.schema.json",
    "roleplay_result": "roleplay_result.schema.json",
    "episode_memory_delta": "episode_memory_delta.schema.json",
    "review_packet": "review_packet.schema.json",
    "review_diff": "review_diff.schema.json",
    "change_proposal": "change_proposal.schema.json",
    "component_version_registry": "component_version_registry.schema.json",
    "replay_evaluation": "replay_evaluation.schema.json",
    "legacy_data_migration": "legacy_data_migration.schema.json",
}


def read_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8-sig"))


def finding(code: str, message: str, path: str = "") -> dict[str, str]:
    item = {"code": code, "message": message}
    if path:
        item["path"] = path
    return item


def schema_errors(kind: str, document: dict[str, Any]) -> list[dict[str, str]]:
    schema = read_json(ROOT / "schemas" / SCHEMAS[kind])
    validator = Draft202012Validator(schema, format_checker=FormatChecker())
    errors = []
    for error in sorted(validator.iter_errors(document), key=lambda value: list(value.path)):
        location = "/".join(str(part) for part in error.path)
        errors.append(finding("SCHEMA", error.message, location))
    return errors


def result(errors: list[dict[str, str]], metrics: dict[str, Any] | None = None) -> dict[str, Any]:
    return {"status": "FAIL" if errors else "PASS", "errors": errors, "metrics": metrics or {}}


def parse_time(value: str) -> datetime:
    return datetime.fromisoformat(value.replace("Z", "+00:00"))


def audit_inner(plan: dict[str, Any], evidence: dict[str, Any], now: datetime) -> dict[str, Any]:
    errors = schema_errors("context_plan", plan) + schema_errors("evidence_pack", evidence)
    if errors:
        return result(errors)
    planned_ids = [item["context_id"] for item in plan["required_context"] + plan["optional_context"]]
    evidence_ids = [item["context_id"] for item in evidence["evidence"]]
    if len(planned_ids) != len(set(planned_ids)) or len(evidence_ids) != len(set(evidence_ids)):
        errors.append(finding("EVIDENCE_ID_DUPLICATE", "Context and evidence IDs must be unique within each artifact."))
    evidence_by_id = {item["context_id"]: item for item in evidence["evidence"]}
    for required in plan["required_context"]:
        item = evidence_by_id.get(required["context_id"])
        if item is None or item["status"] == "missing":
            errors.append(finding("CONTEXT_REQUIRED_MISSING", f"Required context {required['context_id']} is missing."))
            continue
        if item["status"] == "conflicted":
            errors.append(finding("EVIDENCE_CONFLICT_UNRESOLVED", f"Required context {required['context_id']} is conflicted."))
        freshness = required["freshness_hours"]
        if item["status"] == "stale":
            errors.append(finding("STALE_CONTEXT", f"Required context {required['context_id']} is marked stale."))
        elif freshness > 0:
            age_hours = (now - parse_time(item["updated_at"])).total_seconds() / 3600
            if age_hours > freshness:
                errors.append(finding("STALE_CONTEXT", f"Required context {required['context_id']} is {age_hours:.1f} hours old; limit is {freshness}."))
    for conflict in evidence["conflicts"]:
        if conflict["status"] == "unresolved":
            errors.append(finding("EVIDENCE_CONFLICT_UNRESOLVED", f"Unresolved evidence conflict: {conflict['field']}"))
    return result(errors, {"required_context_count": len(plan["required_context"]), "evidence_count": len(evidence["evidence"])})


def audit_state(characters: dict[str, Any], relationships: dict[str, Any], roleplay: dict[str, Any], delta: dict[str, Any]) -> dict[str, Any]:
    errors = []
    for kind, document in [("character_state", characters), ("relationship_state", relationships), ("roleplay_result", roleplay), ("episode_memory_delta", delta)]:
        errors.extend(schema_errors(kind, document))
    if errors:
        return result(errors)
    identifier_sets = [
        ("character_id", [item["character_id"] for item in characters["characters"]]),
        ("relationship_id", [item["relationship_id"] for item in relationships["relationships"]]),
        ("participant.character_id", [item["character_id"] for item in roleplay["participants"]]),
    ]
    for label, identifiers in identifier_sets:
        if len(identifiers) != len(set(identifiers)):
            errors.append(finding("STATE_ID_DUPLICATE", f"Duplicate {label} values are not allowed."))
    character_index = {item["character_id"]: item for item in characters["characters"]}
    relationship_index = {item["relationship_id"]: item for item in relationships["relationships"]}
    participant_ids = [item["character_id"] for item in roleplay["participants"]]
    for participant_id in participant_ids:
        if participant_id not in character_index:
            errors.append(finding("CHARACTER_STATE_DRIFT", f"Roleplay participant {participant_id} has no canonical character state."))
    secret_owners = {
        secret: owner["character_id"]
        for owner in characters["characters"]
        for secret in owner["secrets"]
    }
    for participant in roleplay["participants"]:
        state = character_index.get(participant["character_id"], {})
        authorized = set(state.get("knowledge", [])) | set(state.get("secrets", []))
        for fact in participant["known_facts"]:
            owner_id = secret_owners.get(fact)
            if owner_id and owner_id != participant["character_id"] and fact not in authorized:
                errors.append(finding("CHARACTER_KNOWLEDGE_LEAK", f"{participant['character_id']} knows secret owned by {owner_id} without canonical knowledge evidence."))
    if len(participant_ids) >= 3:
        for participant_id in participant_ids:
            state = character_index.get(participant_id, {})
            for field in ("location", "current_goal", "emotional_state", "knowledge", "secrets", "inventory"):
                if field not in state or state[field] in (None, ""):
                    errors.append(finding("CHARACTER_STATE_DRIFT", f"Three-character scene requires {participant_id}.{field}."))
    if delta["base_state_version"] != characters["state_version"] or delta["base_state_version"] != relationships["state_version"]:
        errors.append(finding("CHARACTER_STATE_DRIFT", "Delta base version does not match character and relationship state versions."))
    for change in delta["changes"]:
        target = character_index.get(change["target_id"]) if change["target_type"] == "character" else relationship_index.get(change["target_id"]) if change["target_type"] == "relationship" else None
        if target is None and change["target_type"] != "canon_decision":
            errors.append(finding("CHARACTER_STATE_DRIFT", f"Delta target {change['target_id']} does not exist."))
        elif target is not None and target.get(change["field"]) != change["before"]:
            errors.append(finding("CHARACTER_STATE_DRIFT", f"Delta before value does not match {change['target_id']}.{change['field']}."))
    approval = delta["human_approval"]
    if delta["continuity_check"]["status"] != "pass" or approval["status"] != "approved" or not approval["approval_id"]:
        errors.append(finding("CANON_DELTA_UNAPPROVED", "Episode memory delta requires continuity PASS and explicit human approval."))
    return result(errors, {"participant_count": len(participant_ids), "delta_change_count": len(delta["changes"])})


def audit_review(packet: dict[str, Any]) -> dict[str, Any]:
    errors = schema_errors("review_packet", packet)
    if errors:
        return result(errors)
    outcome = packet["human_outcome"]
    draft_path = Path(packet["draft_path"])
    final_path = Path(packet["final_path"])
    if not draft_path.is_absolute():
        draft_path = ROOT / draft_path
    if not final_path.is_absolute():
        final_path = ROOT / final_path
    if not packet["draft_path"] or not packet["final_path"] or draft_path.resolve() == final_path.resolve() or not draft_path.is_file() or not final_path.is_file() or outcome["status"] in {"pending", "held"} or outcome["reviewed_at"] is None:
        errors.append(finding("REVIEW_PAIR_MISSING", "A completed review requires distinct explicit draft and final paths."))
    return result(errors, {"context_source_count": len(packet["context_used"])})


def audit_control(proposal: dict[str, Any], registry: dict[str, Any]) -> dict[str, Any]:
    errors = schema_errors("change_proposal", proposal) + schema_errors("component_version_registry", registry)
    if errors:
        return result(errors)
    status = proposal["status"]
    if status not in {"proposed", "rejected"} and proposal["approvals"]["candidate"]["status"] != "approved":
        errors.append(finding("PROMOTION_APPROVAL_MISSING", "Candidate approval is required before candidate or canary state."))
    if status in {"candidate", "canary", "promoted"} and proposal["replay"]["status"] != "pass":
        errors.append(finding("REGRESSION_DETECTED", "Offline replay must pass before candidate activation."))
    if proposal["replay"]["regressions"]:
        errors.append(finding("REGRESSION_DETECTED", "Replay contains regressions."))
    if status == "promoted":
        if proposal["canary"]["status"] != "pass" or proposal["canary"]["completed_tasks"] != 1:
            errors.append(finding("REGRESSION_DETECTED", "Exactly one passing canary task is required before promotion."))
        if proposal["approvals"]["promotion"]["status"] != "approved":
            errors.append(finding("PROMOTION_APPROVAL_MISSING", "Second human approval is required for promotion."))
    return result(errors, {"proposal_status": status, "component_count": len(registry["components"])})


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)
    validate = sub.add_parser("validate")
    validate.add_argument("kind", choices=sorted(SCHEMAS))
    validate.add_argument("artifact", type=Path)
    inner = sub.add_parser("inner")
    inner.add_argument("context_plan", type=Path); inner.add_argument("evidence_pack", type=Path); inner.add_argument("--now")
    state = sub.add_parser("state")
    state.add_argument("character_state", type=Path); state.add_argument("relationship_state", type=Path); state.add_argument("roleplay_result", type=Path); state.add_argument("episode_memory_delta", type=Path)
    review = sub.add_parser("review"); review.add_argument("review_packet", type=Path)
    control = sub.add_parser("control"); control.add_argument("change_proposal", type=Path); control.add_argument("version_registry", type=Path)
    args = parser.parse_args()
    try:
        if args.command == "validate":
            output = result(schema_errors(args.kind, read_json(args.artifact)))
        elif args.command == "inner":
            now = parse_time(args.now) if args.now else datetime.now(timezone.utc)
            output = audit_inner(read_json(args.context_plan), read_json(args.evidence_pack), now)
        elif args.command == "state":
            output = audit_state(read_json(args.character_state), read_json(args.relationship_state), read_json(args.roleplay_result), read_json(args.episode_memory_delta))
        elif args.command == "review":
            output = audit_review(read_json(args.review_packet))
        else:
            output = audit_control(read_json(args.change_proposal), read_json(args.version_registry))
    except (OSError, json.JSONDecodeError, ValueError) as exc:
        output = result([finding("INPUT", str(exc))])
    print(json.dumps(output, ensure_ascii=False, indent=2))
    return 0 if output["status"] == "PASS" else 1


if __name__ == "__main__":
    sys.exit(main())

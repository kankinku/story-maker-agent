#!/usr/bin/env python3
"""Manage approved candidate, canary, promotion, and rollback state transitions."""
from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator

ROOT = Path(__file__).resolve().parents[1]


def load(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8-sig"))


def now() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def fail(code: str, message: str) -> int:
    print(json.dumps({"status": "FAIL", "errors": [{"code": code, "message": message}]}, ensure_ascii=False, indent=2)); return 1


def approval(proposal: dict[str, Any], stage: str) -> bool:
    item = proposal.get("approvals", {}).get(stage, {})
    return item.get("status") == "approved" and bool(item.get("approval_id")) and bool(item.get("approved_by"))


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("command", choices=["candidate", "canary", "promote", "rollback"])
    parser.add_argument("--registry", type=Path, required=True); parser.add_argument("--proposal", type=Path, required=True)
    parser.add_argument("--component-id", required=True); parser.add_argument("--candidate-version"); parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    try:
        registry, proposal = load(args.registry), load(args.proposal)
    except (OSError, json.JSONDecodeError) as exc:
        return fail("INPUT", str(exc))
    for document, schema_name in [(registry, "component_version_registry.schema.json"), (proposal, "change_proposal.schema.json")]:
        schema = load(ROOT / "schemas" / schema_name)
        schema_errors = list(Draft202012Validator(schema).iter_errors(document))
        if schema_errors:
            return fail("SCHEMA", "; ".join(error.message for error in schema_errors))
    component = next((item for item in registry.get("components", []) if item.get("component_id") == args.component_id), None)
    if component is None:
        return fail("INPUT", f"Unknown component: {args.component_id}")
    proposal_id = proposal.get("proposal_id", "")
    event = ""
    if args.command == "candidate":
        if not args.candidate_version:
            return fail("INPUT", "--candidate-version is required")
        if not approval(proposal, "candidate"):
            return fail("PROMOTION_APPROVAL_MISSING", "Candidate approval is required.")
        if proposal.get("replay", {}).get("status") != "pass" or proposal.get("replay", {}).get("regressions"):
            return fail("REGRESSION_DETECTED", "Passing replay without regressions is required.")
        component.update({"candidate_version": args.candidate_version, "status": "candidate", "proposal_id": proposal_id}); proposal["status"] = "candidate"; event = "candidate_created"
    elif args.command == "canary":
        if component.get("status") != "candidate" or proposal.get("status") != "candidate":
            return fail("INPUT", "A candidate version must exist before canary.")
        component["status"] = "canary"; proposal["status"] = "canary"; event = "canary_started"
    elif args.command == "promote":
        if component.get("status") != "canary" or proposal.get("canary", {}).get("status") != "pass" or proposal.get("canary", {}).get("completed_tasks") != 1:
            return fail("REGRESSION_DETECTED", "Exactly one passing canary task is required.")
        if not approval(proposal, "promotion"):
            return fail("PROMOTION_APPROVAL_MISSING", "Promotion approval is required.")
        component["previous_version"] = component["active_version"]; component["active_version"] = component["candidate_version"]; component["candidate_version"] = None; component["status"] = "active"; component["proposal_id"] = None
        proposal["status"] = "promoted"; event = "promoted"
    else:
        if not component.get("previous_version"):
            return fail("INPUT", "No previous version is available for rollback.")
        replay_failed = proposal.get("replay", {}).get("status") == "fail" or bool(proposal.get("replay", {}).get("regressions"))
        canary_failed = proposal.get("canary", {}).get("status") == "fail"
        if not replay_failed and not canary_failed:
            return fail("ROLLBACK_REASON_MISSING", "Rollback requires recorded replay or canary regression evidence.")
        rolled_back = component["active_version"]; component["active_version"] = component["previous_version"]; component["previous_version"] = rolled_back; component["candidate_version"] = None; component["status"] = "rolled_back"; component["proposal_id"] = proposal_id
        proposal["status"] = "rolled_back"; event = "rolled_back"
    stage = "promotion" if args.command == "promote" else "candidate"
    approval_id = proposal.get("approvals", {}).get(stage, {}).get("approval_id", "")
    registry.setdefault("history", []).append({"event": event, "component_id": args.component_id, "version": component["active_version"] if event in {"promoted", "rolled_back"} else component["candidate_version"], "proposal_id": proposal_id, "approval_id": approval_id, "timestamp": now()})
    if not args.dry_run:
        args.registry.write_text(json.dumps(registry, ensure_ascii=False, indent=2), encoding="utf-8")
        args.proposal.write_text(json.dumps(proposal, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps({"status": "PASS", "errors": [], "event": event, "dry_run": args.dry_run, "component": component}, ensure_ascii=False, indent=2)); return 0


if __name__ == "__main__":
    sys.exit(main())

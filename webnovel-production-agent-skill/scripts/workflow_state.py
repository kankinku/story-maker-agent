#!/usr/bin/env python3
"""Read and write the project .omx workflow state for webnovel production."""
from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


WORKFLOW = "webnovel-production-workflow"


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def state_path(project_root: Path) -> Path:
    return project_root / ".omx" / "state" / f"{WORKFLOW}.json"


def default_state() -> dict[str, Any]:
    return {
        "active": True,
        "status": "running",
        "workflow": WORKFLOW,
        "phase": "intake",
        "project_id": "",
        "project_version": "",
        "story_bible_version": "",
        "last_gate": "G0",
        "goal": "",
        "exit_when": [],
        "iteration": 0,
        "max_iterations": 0,
        "check_commands": [],
        "last_check_result": "",
        "selected_failure": "",
        "selected_agent": "",
        "next_action": "",
        "blocked_reason": "",
        "context_plan_path": "",
        "evidence_pack_path": "",
        "character_state_path": "",
        "relationship_state_path": "",
        "review_packet_path": "",
        "change_proposal_path": "",
        "version_registry_path": "",
        "approval_state": "pending",
        "canary_state": "pending",
        "updated_at": utc_now(),
    }


def load_state(path: Path) -> dict[str, Any]:
    if not path.exists():
        return default_state()
    loaded = json.loads(path.read_text(encoding="utf-8-sig"))
    state = {**default_state(), **loaded}
    if "status" not in loaded:
        state["status"] = "running" if state["active"] else "blocked" if state["blocked_reason"] else "completed"
    return state


def save_state(path: Path, state: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    state["updated_at"] = utc_now()
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(json.dumps(state, ensure_ascii=False, indent=2), encoding="utf-8")
    temporary.replace(path)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--project-root", type=Path, default=Path.cwd().parent)
    subparsers = parser.add_subparsers(dest="command", required=True)

    subparsers.add_parser("show")
    subparsers.add_parser("init")

    update = subparsers.add_parser("update")
    update.add_argument("--phase")
    update.add_argument("--goal")
    update.add_argument("--last-gate")
    update.add_argument("--iteration", type=int)
    update.add_argument("--max-iterations", type=int)
    update.add_argument("--selected-failure")
    update.add_argument("--selected-agent")
    update.add_argument("--next-action")
    update.add_argument("--blocked-reason")
    update.add_argument("--check-command", action="append", default=[])
    update.add_argument("--exit-when", action="append", default=[])
    update.add_argument("--last-check-result")
    update.add_argument("--context-plan-path")
    update.add_argument("--evidence-pack-path")
    update.add_argument("--character-state-path")
    update.add_argument("--relationship-state-path")
    update.add_argument("--review-packet-path")
    update.add_argument("--change-proposal-path")
    update.add_argument("--version-registry-path")
    update.add_argument("--approval-state", choices=["pending", "approved", "rejected"])
    update.add_argument("--canary-state", choices=["pending", "running", "pass", "fail"])
    update.add_argument("--complete", action="store_true")
    update.add_argument("--blocked", action="store_true")

    args = parser.parse_args()
    project_root = args.project_root.resolve()
    path = state_path(project_root)
    state = load_state(path)

    if args.command == "init":
        state = default_state()
        save_state(path, state)
    elif args.command == "update":
        if args.complete and args.blocked or state["status"] in {"completed", "blocked"}:
            print(json.dumps({"status": "FAIL", "errors": [{"code": "INVALID_STATE_TRANSITION", "message": f"Cannot update terminal workflow state: {state['status']}"}]}, ensure_ascii=False, indent=2))
            return 1
        for attr, key in [
            ("phase", "phase"),
            ("goal", "goal"),
            ("last_gate", "last_gate"),
            ("iteration", "iteration"),
            ("max_iterations", "max_iterations"),
            ("selected_failure", "selected_failure"),
            ("selected_agent", "selected_agent"),
            ("next_action", "next_action"),
            ("blocked_reason", "blocked_reason"),
            ("last_check_result", "last_check_result"),
            ("context_plan_path", "context_plan_path"),
            ("evidence_pack_path", "evidence_pack_path"),
            ("character_state_path", "character_state_path"),
            ("relationship_state_path", "relationship_state_path"),
            ("review_packet_path", "review_packet_path"),
            ("change_proposal_path", "change_proposal_path"),
            ("version_registry_path", "version_registry_path"),
            ("approval_state", "approval_state"),
            ("canary_state", "canary_state"),
        ]:
            value = getattr(args, attr)
            if value is not None:
                state[key] = value
        if args.check_command:
            state["check_commands"] = args.check_command
        if args.exit_when:
            state["exit_when"] = args.exit_when
        if args.complete:
            state["active"] = False
            state["status"] = "completed"
            state["blocked_reason"] = ""
        if args.blocked:
            state["active"] = False
            state["status"] = "blocked"
            state["blocked_reason"] = state.get("blocked_reason") or "blocked"
        save_state(path, state)

    print(json.dumps(state, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())

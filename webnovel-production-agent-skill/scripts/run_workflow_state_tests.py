#!/usr/bin/env python3
"""Verify workflow-state transition invariants and resumable control-loop fields."""
from __future__ import annotations

import json
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "workflow_state.py"


def run(root: Path, *args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run([sys.executable, str(SCRIPT), "--project-root", str(root), *args], capture_output=True, text=True, encoding="utf-8")


def main() -> int:
    results = []
    with tempfile.TemporaryDirectory() as directory:
        root = Path(directory)
        init = run(root, "init")
        state = json.loads(init.stdout)
        resumable = all(key in state for key in ["context_plan_path", "evidence_pack_path", "character_state_path", "relationship_state_path", "review_packet_path", "change_proposal_path", "version_registry_path", "approval_state", "canary_state"])
        results.append({"case": "control_loop_fields_are_resumable", "passed": init.returncode == 0 and resumable})
        complete = run(root, "update", "--complete", "--last-check-result", "PASS")
        blocked_after_complete = run(root, "update", "--blocked", "--blocked-reason", "late block")
        blocked_output = json.loads(blocked_after_complete.stdout)
        invalid_transition = complete.returncode == 0 and blocked_after_complete.returncode != 0 and any(item["code"] == "INVALID_STATE_TRANSITION" for item in blocked_output.get("errors", []))
        results.append({"case": "completed_state_cannot_be_blocked", "passed": invalid_transition})
    failed = sum(not item["passed"] for item in results)
    print(json.dumps({"status": "FAIL" if failed else "PASS", "total": len(results), "failed": failed, "results": results}, ensure_ascii=False, indent=2))
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())

#!/usr/bin/env python3
"""Run the Korean manuscript completion guard and write a JSON report."""
from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("manuscript", type=Path, help="Manuscript file to guard")
    parser.add_argument("--guard", type=Path, help="Path to ai_tell_guard.py")
    parser.add_argument("--report", type=Path, help="JSON report path")
    parser.add_argument("--humanized", action="store_true", help="Caller confirms $humanize-korean was already applied")
    parser.add_argument("--humanization-report", type=Path, help="Hash-bound JSON evidence emitted after $humanize-korean")
    parser.add_argument("--allow-missing-guard", action="store_true", help="Write BLOCKED report instead of failing hard when guard is unavailable")
    args = parser.parse_args()

    manuscript = args.manuscript.resolve()
    report_path = args.report or manuscript.with_suffix(manuscript.suffix + ".guard-report.json")
    report: dict[str, Any] = {
        "checked_at": utc_now(),
        "manuscript": str(manuscript),
        "humanize_korean": {
            "required": True,
            "status": "confirmed" if args.humanized else "required_external_skill",
        },
        "ai_tell_guard": {
            "required": True,
            "status": "not_run",
            "guard_path": str(args.guard.resolve()) if args.guard else "",
            "exit_code": None,
            "stdout": "",
            "stderr": "",
        },
        "status": "PENDING",
        "failure_code": "",
        "blocked_reason": "",
    }

    if not manuscript.exists():
        report["status"] = "FAIL"
        report["blocked_reason"] = "manuscript file does not exist"
        report_path.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
        print(json.dumps(report, ensure_ascii=False, indent=2))
        return 2

    if not args.humanized:
        report["status"] = "BLOCKED"
        report["failure_code"] = "HUMANIZATION_EVIDENCE_MISSING"
        report["blocked_reason"] = "$humanize-korean must be applied before final manuscript completion"
        report_path.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
        print(json.dumps(report, ensure_ascii=False, indent=2))
        return 1

    if args.humanization_report is None or not args.humanization_report.is_file():
        report["status"] = "BLOCKED"
        report["failure_code"] = "HUMANIZATION_EVIDENCE_MISSING"
        report["blocked_reason"] = "A hash-bound humanization report is required; --humanized alone is not evidence"
        report_path.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
        print(json.dumps(report, ensure_ascii=False, indent=2))
        return 1
    try:
        humanization = json.loads(args.humanization_report.read_text(encoding="utf-8-sig"))
    except (OSError, json.JSONDecodeError) as exc:
        report["status"] = "FAIL"; report["failure_code"] = "HUMANIZATION_EVIDENCE_INVALID"; report["blocked_reason"] = str(exc)
        report_path.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8"); print(json.dumps(report, ensure_ascii=False, indent=2)); return 1
    manuscript_hash = "sha256:" + hashlib.sha256(manuscript.read_bytes()).hexdigest()
    if humanization.get("status") != "PASS" or humanization.get("skill") != "humanize-korean" or Path(humanization.get("manuscript_path", "")).resolve() != manuscript or humanization.get("manuscript_hash") != manuscript_hash:
        report["status"] = "FAIL"; report["failure_code"] = "HUMANIZATION_EVIDENCE_INVALID"; report["blocked_reason"] = "Humanization report does not match the current manuscript path and hash"
        report_path.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8"); print(json.dumps(report, ensure_ascii=False, indent=2)); return 1
    report["humanize_korean"].update({"status": "verified", "report_path": str(args.humanization_report.resolve()), "manuscript_hash": manuscript_hash})

    guard = args.guard.resolve() if args.guard else None
    if guard is None or not guard.exists():
        report["status"] = "BLOCKED"
        report["blocked_reason"] = "ai_tell_guard.py is unavailable"
        report_path.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
        print(json.dumps(report, ensure_ascii=False, indent=2))
        return 0 if args.allow_missing_guard else 1

    cmd = [
        sys.executable,
        str(guard),
        str(manuscript),
        "--output",
        str(report_path.with_suffix(".ai-tell.json")),
        "--fail-on-s1",
    ]
    completed = subprocess.run(cmd, capture_output=True, text=True)
    report["ai_tell_guard"].update({
        "status": "PASS" if completed.returncode == 0 else "FAIL",
        "exit_code": completed.returncode,
        "stdout": completed.stdout,
        "stderr": completed.stderr,
        "command": cmd,
    })
    report["status"] = "PASS" if completed.returncode == 0 else "FAIL"
    report_path.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return completed.returncode


if __name__ == "__main__":
    sys.exit(main())

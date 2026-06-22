#!/usr/bin/env python3
"""Run pass/fail fixtures for the source-rewrite fidelity auditor."""
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def run(name: str, expected_exit: int, expected_codes: set[str]) -> dict[str, object]:
    process = subprocess.run(
        [sys.executable, str(ROOT / "scripts" / "audit_rewrite_fidelity.py"), str(ROOT / "tests" / "fixtures" / name)],
        capture_output=True,
        text=True,
        encoding="utf-8",
    )
    payload = json.loads(process.stdout)
    actual_codes = {item["code"] for item in payload.get("errors", [])}
    return {
        "fixture": name,
        "passed": process.returncode == expected_exit and expected_codes <= actual_codes,
        "status": payload.get("status"),
        "error_codes": sorted(actual_codes),
    }


def main() -> int:
    results = [
        run("rewrite_fidelity.pass.json", 0, set()),
        run(
            "rewrite_fidelity.fail.json",
            1,
            {
                "REWRITE_EVENT_MISSING",
                "REWRITE_EVENT_INVENTED",
                "REWRITE_EVENT_REORDERED",
                "REWRITE_ENTITY_DRIFT",
                "REWRITE_QUOTE_DRIFT",
                "REWRITE_SOURCE_EVIDENCE_INVALID",
            },
        ),
    ]
    passed = all(item["passed"] for item in results)
    print(json.dumps({"status": "PASS" if passed else "FAIL", "results": results}, ensure_ascii=False, indent=2))
    return 0 if passed else 1


if __name__ == "__main__":
    raise SystemExit(main())

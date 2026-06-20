#!/usr/bin/env python3
"""Verify every supported intent has one deterministic current workflow route."""
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def main() -> int:
    cases = json.loads((ROOT / "tests" / "intent_route_cases.json").read_text(encoding="utf-8"))["cases"]
    results = []
    for case in cases:
        run = subprocess.run([sys.executable, str(ROOT / "scripts" / "route_intent.py"), case["intent"]], capture_output=True, text=True, encoding="utf-8")
        try:
            output = json.loads(run.stdout)
        except json.JSONDecodeError:
            output = {}
        passed = run.returncode == 0 and output.get("steps") == case["steps"] and output.get("primary_role") == case["primary_role"]
        results.append({"intent": case["intent"], "passed": passed, "actual": output})
    failed = sum(not item["passed"] for item in results)
    print(json.dumps({"status": "FAIL" if failed else "PASS", "total": len(results), "failed": failed, "results": results}, ensure_ascii=False, indent=2))
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())

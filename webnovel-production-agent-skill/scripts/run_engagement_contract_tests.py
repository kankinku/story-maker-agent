#!/usr/bin/env python3
"""Run pass/fail fixtures for the engagement scene-contract auditor."""
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def run(name: str, story_bible_name: str, expected: int) -> dict[str, object]:
    fixture = ROOT / "tests" / "fixtures" / name
    story_bible = ROOT / "tests" / "fixtures" / story_bible_name
    process = subprocess.run(
        [sys.executable, str(ROOT / "scripts" / "audit_engagement_contract.py"), str(fixture), "--story-bible", str(story_bible)],
        capture_output=True,
        text=True,
        encoding="utf-8",
    )
    payload = json.loads(process.stdout)
    return {"fixture": name, "story_bible": story_bible_name, "passed": process.returncode == expected, "status": payload.get("status")}


def main() -> int:
    results = [
        run("engagement_contract.pass.json", "engagement_story_bible.pass.json", 0),
        run("engagement_contract.fail.json", "engagement_story_bible.fail.json", 1),
    ]
    passed = all(item["passed"] for item in results)
    print(json.dumps({"status": "PASS" if passed else "FAIL", "results": results}, ensure_ascii=False, indent=2))
    return 0 if passed else 1


if __name__ == "__main__":
    raise SystemExit(main())

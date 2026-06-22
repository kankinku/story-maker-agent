#!/usr/bin/env python3
"""Run pass/fail fixtures for the engagement scene-contract auditor."""
from __future__ import annotations

import json
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def run_path(fixture: Path, story_bible_name: str, expected: int, label: str) -> dict[str, object]:
    story_bible = ROOT / "tests" / "fixtures" / story_bible_name
    process = subprocess.run(
        [sys.executable, str(ROOT / "scripts" / "audit_engagement_contract.py"), str(fixture), "--story-bible", str(story_bible)],
        capture_output=True,
        text=True,
        encoding="utf-8",
    )
    payload = json.loads(process.stdout)
    return {"fixture": label, "story_bible": story_bible_name, "passed": process.returncode == expected, "status": payload.get("status")}


def run(name: str, story_bible_name: str, expected: int) -> dict[str, object]:
    return run_path(ROOT / "tests" / "fixtures" / name, story_bible_name, expected, name)


def main() -> int:
    with tempfile.TemporaryDirectory() as directory:
        source = json.loads((ROOT / "tests" / "fixtures" / "engagement_contract.pass.json").read_text(encoding="utf-8"))
        no_exposition = json.loads(json.dumps(source))
        no_exposition["scenes"][0].pop("exposition", None)
        no_exposition_path = Path(directory) / "no-exposition.json"
        no_exposition_path.write_text(json.dumps(no_exposition, ensure_ascii=False), encoding="utf-8")

        partial_exposition = json.loads(json.dumps(source))
        partial_exposition["scenes"][0]["exposition"] = {"trigger": "잠긴 문을 열어야 한다.", "immediate_use": ""}
        partial_exposition_path = Path(directory) / "partial-exposition.json"
        partial_exposition_path.write_text(json.dumps(partial_exposition, ensure_ascii=False), encoding="utf-8")

        results = [
            run("engagement_contract.pass.json", "engagement_story_bible.pass.json", 0),
            run("engagement_contract.fail.json", "engagement_story_bible.fail.json", 1),
            run_path(no_exposition_path, "engagement_story_bible.pass.json", 0, "no_exposition_is_valid"),
            run_path(partial_exposition_path, "engagement_story_bible.pass.json", 1, "partial_exposition_is_invalid"),
        ]
    passed = all(item["passed"] for item in results)
    print(json.dumps({"status": "PASS" if passed else "FAIL", "results": results}, ensure_ascii=False, indent=2))
    return 0 if passed else 1


if __name__ == "__main__":
    raise SystemExit(main())

#!/usr/bin/env python3
"""Rehydrate the single-JSON export and run isolated dependency smoke tests."""
from __future__ import annotations

import base64
import json
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
EXPORT = ROOT / "dist" / "webnovel-production-loop.skill.json"


def run(command: list[str]) -> dict[str, object]:
    process = subprocess.run(command, capture_output=True, text=True, encoding="utf-8")
    return {
        "command": command[1],
        "passed": process.returncode == 0,
        "exit_code": process.returncode,
        "stderr": process.stderr.strip(),
    }


def main() -> int:
    export = json.loads(EXPORT.read_text(encoding="utf-8"))
    scripts = json.loads(export["data"]["scripts"])
    assets = json.loads(export["data"]["assets"])
    with tempfile.TemporaryDirectory() as directory:
        root = Path(directory)
        (root / "scripts").mkdir(parents=True, exist_ok=True)
        for item in scripts:
            (root / "scripts" / item["filename"]).write_text(item["content"], encoding="utf-8")
        for item in assets:
            path = root / item["path"]
            path.parent.mkdir(parents=True, exist_ok=True)
            payload = item["content"].encode("utf-8") if item["encoding"] == "utf-8" else base64.b64decode(item["content"])
            path.write_bytes(payload)
        results = [
            run([sys.executable, str(root / "scripts" / "validate_project.py"), str(root / "tests" / "fixtures" / "valid_project.json")]),
            run([
                sys.executable,
                str(root / "scripts" / "audit_engagement_contract.py"),
                str(root / "tests" / "fixtures" / "engagement_contract.pass.json"),
                "--story-bible",
                str(root / "tests" / "fixtures" / "engagement_story_bible.pass.json"),
            ]),
            run([
                sys.executable,
                str(root / "scripts" / "run_semantic_rubric.py"),
                str(root / "tests" / "fixtures" / "semantic_rubric_scores.pass.json"),
                "--include-style",
            ]),
            run([
                sys.executable,
                str(root / "scripts" / "audit_rewrite_fidelity.py"),
                str(root / "tests" / "fixtures" / "rewrite_fidelity.pass.json"),
            ]),
        ]
    passed = all(item["passed"] for item in results)
    print(json.dumps({"status": "PASS" if passed else "FAIL", "results": results}, ensure_ascii=False, indent=2))
    return 0 if passed else 1


if __name__ == "__main__":
    raise SystemExit(main())

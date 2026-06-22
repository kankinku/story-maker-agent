#!/usr/bin/env python3
"""Test semantic rubric score and per-dimension evidence gates."""
from __future__ import annotations

import json
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "run_semantic_rubric.py"
FIXTURE = ROOT / "tests" / "fixtures" / "semantic_rubric_scores.pass.json"


def execute(path: Path) -> tuple[int, dict[str, object]]:
    process = subprocess.run(
        [sys.executable, str(SCRIPT), str(path), "--include-style"],
        capture_output=True,
        text=True,
        encoding="utf-8",
    )
    return process.returncode, json.loads(process.stdout)


def main() -> int:
    pass_code, pass_result = execute(FIXTURE)
    source = json.loads(FIXTURE.read_text(encoding="utf-8"))
    source.pop("evidence_by_dimension", None)
    with tempfile.TemporaryDirectory() as directory:
        missing_path = Path(directory) / "missing-evidence.json"
        missing_path.write_text(json.dumps(source, ensure_ascii=False), encoding="utf-8")
        missing_code, missing_result = execute(missing_path)
    missing_codes = {item.get("code") for item in missing_result.get("errors", [])}
    results = [
        {"case": "scores_with_dimension_evidence_pass", "passed": pass_code == 0 and pass_result.get("status") == "PASS"},
        {"case": "scores_without_dimension_evidence_fail", "passed": missing_code == 1 and "RUBRIC_EVIDENCE_MISSING" in missing_codes},
    ]
    passed = all(item["passed"] for item in results)
    print(json.dumps({"status": "PASS" if passed else "FAIL", "results": results}, ensure_ascii=False, indent=2))
    return 0 if passed else 1


if __name__ == "__main__":
    raise SystemExit(main())

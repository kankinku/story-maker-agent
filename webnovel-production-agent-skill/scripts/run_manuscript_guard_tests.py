#!/usr/bin/env python3
"""Verify manuscript completion requires hash-bound humanization evidence."""
from __future__ import annotations

import hashlib
import json
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def main() -> int:
    results = []
    with tempfile.TemporaryDirectory() as directory:
        root = Path(directory); manuscript = root / "episode.txt"; report = root / "humanization.json"
        manuscript.write_text("검증할 원고입니다.", encoding="utf-8")
        base = [sys.executable, str(ROOT / "scripts" / "run_manuscript_guard.py"), str(manuscript), "--guard", str(ROOT / "tests" / "fixtures" / "stub_ai_tell_guard.py"), "--humanized"]
        missing = subprocess.run(base, capture_output=True, text=True, encoding="utf-8")
        results.append({"case": "flag_alone_cannot_confirm_humanization", "passed": missing.returncode != 0 and "HUMANIZATION_EVIDENCE_MISSING" in missing.stdout})
        digest = "sha256:" + hashlib.sha256(manuscript.read_bytes()).hexdigest()
        report.write_text(json.dumps({"status": "PASS", "manuscript_path": str(manuscript.resolve()), "manuscript_hash": digest, "skill": "humanize-korean"}), encoding="utf-8")
        verified = subprocess.run(base + ["--humanization-report", str(report)], capture_output=True, text=True, encoding="utf-8")
        results.append({"case": "hash_bound_humanization_evidence_passes", "passed": verified.returncode == 0 and json.loads(verified.stdout)["status"] == "PASS"})
    failed = sum(not item["passed"] for item in results)
    print(json.dumps({"status": "FAIL" if failed else "PASS", "total": len(results), "failed": failed, "results": results}, ensure_ascii=False, indent=2))
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())

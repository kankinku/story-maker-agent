#!/usr/bin/env python3
"""Verify top-level project and output contracts require context-compounding evidence."""
from __future__ import annotations

import copy
import json
import subprocess
import sys
import tempfile
from pathlib import Path

from jsonschema import Draft202012Validator

ROOT = Path(__file__).resolve().parents[1]


def errors(schema_name: str, document: dict) -> list:
    schema = json.loads((ROOT / "schemas" / schema_name).read_text(encoding="utf-8"))
    return list(Draft202012Validator(schema).iter_errors(document))


def main() -> int:
    project = json.loads((ROOT / "tests" / "fixtures" / "valid_project.json").read_text(encoding="utf-8"))
    output = json.loads((ROOT / "tests" / "fixtures" / "valid_output.json").read_text(encoding="utf-8"))
    project_without_context = copy.deepcopy(project); project_without_context.pop("context_compounding", None)
    output_without_evidence = copy.deepcopy(output)
    for key in ["evidence", "component_versions", "uncertainties", "approval_state"]:
        output_without_evidence.pop(key, None)
    results = [
        {"case": "project_requires_context_compounding", "passed": bool(errors("project.schema.json", project_without_context))},
        {"case": "output_requires_evidence_and_approval", "passed": bool(errors("output.schema.json", output_without_evidence))},
    ]
    with tempfile.TemporaryDirectory() as directory:
        bom_path = Path(directory) / "project.json"
        bom_path.write_text(json.dumps(project, ensure_ascii=False), encoding="utf-8-sig")
        run = subprocess.run([sys.executable, str(ROOT / "scripts" / "validate_project.py"), str(bom_path), "--compact"], capture_output=True, text=True, encoding="utf-8")
        results.append({"case": "project_validator_accepts_utf8_bom", "passed": run.returncode == 0})
    failed = sum(not item["passed"] for item in results)
    print(json.dumps({"status": "FAIL" if failed else "PASS", "total": len(results), "failed": failed, "results": results}, ensure_ascii=False, indent=2))
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())

#!/usr/bin/env python3
"""Run the package validation suite and generate TEST_REPORT.json."""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import subprocess
import sys
import tempfile
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]


def utc_now() -> str:
    return datetime.now(timezone.utc).date().isoformat()


def run_command(command: list[str]) -> dict[str, Any]:
    environment = os.environ.copy()
    environment["PYTHONUTF8"] = "1"
    completed = subprocess.run(command, cwd=ROOT, capture_output=True, text=True, encoding="utf-8", errors="replace", env=environment)
    return {
        "command": command,
        "exit_code": completed.returncode,
        "stdout": completed.stdout,
        "stderr": completed.stderr,
        "status": "PASS" if completed.returncode == 0 else "FAIL",
    }


def parse_json_stdout(result: dict[str, Any]) -> dict[str, Any]:
    try:
        return json.loads(result.get("stdout", "") or "{}")
    except json.JSONDecodeError:
        return {}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--project-root", type=Path, default=ROOT.parent)
    parser.add_argument("--output", type=Path, default=ROOT / "TEST_REPORT.json")
    args = parser.parse_args()

    manifest = json.loads((ROOT / "manifest.json").read_text(encoding="utf-8"))
    with tempfile.TemporaryDirectory() as tmpdir:
        guard_report = str(Path(tmpdir) / "manuscript-guard-smoke.json")
        humanization_report = Path(tmpdir) / "humanization-smoke.json"
        manuscript_path = (ROOT / "tests" / "fixtures" / "sample_manuscript.txt").resolve()
        humanization_report.write_text(json.dumps({"status": "PASS", "skill": "humanize-korean", "manuscript_path": str(manuscript_path), "manuscript_hash": "sha256:" + hashlib.sha256(manuscript_path.read_bytes()).hexdigest()}), encoding="utf-8")
        calibration_report = str(Path(tmpdir) / "sample-calibration-smoke.json")
        commands = [
            [sys.executable, "scripts/build_export.py", "--output", "dist/webnovel-production-loop.skill.json"],
            [sys.executable, "scripts/audit_skill_package.py", "--project-root", str(args.project_root.resolve())],
            [sys.executable, "scripts/validate_project.py", "tests/fixtures/valid_project.json", "--compact"],
            [sys.executable, "scripts/audit_narrative.py", "tests/fixtures/valid_project.json"],
            [sys.executable, "scripts/audit_lexicon.py"],
            [sys.executable, "scripts/audit_style_profile.py", "tests/fixtures/style_audit_sample.txt"],
            [sys.executable, "scripts/run_semantic_rubric.py", "tests/fixtures/semantic_rubric_scores.pass.json", "--include-style"],
            [
                sys.executable,
                "scripts/calibrate_from_samples.py",
                "tests/fixtures/sample_corpus",
                "--output",
                calibration_report,
                "--top",
                "10",
                "--min-count",
                "1",
            ],
            [sys.executable, "scripts/run_context_compounding_tests.py"],
            [sys.executable, "scripts/audit_current_system_alignment.py", "--project-root", str(args.project_root.resolve())],
            [sys.executable, "scripts/run_regression.py", "tests/regression_cases.json"],
            [
                sys.executable,
                "scripts/run_manuscript_guard.py",
                "tests/fixtures/sample_manuscript.txt",
                "--guard",
                "tests/fixtures/stub_ai_tell_guard.py",
                "--report",
                guard_report,
                "--humanized",
                "--humanization-report",
                str(humanization_report),
            ],
            [sys.executable, "scripts/run_intent_route_tests.py"],
            [sys.executable, "scripts/run_contract_tests.py"],
            [sys.executable, "scripts/run_workflow_state_tests.py"],
            [sys.executable, "scripts/run_manuscript_guard_tests.py"],
            [sys.executable, "scripts/run_engagement_contract_tests.py"],
            [sys.executable, "scripts/run_semantic_rubric_tests.py"],
            [sys.executable, "scripts/audit_workspace_projects.py", "--project-root", str(args.project_root.resolve())],
            [sys.executable, "scripts/run_portable_export_tests.py"],
        ]
        results = [run_command(command) for command in commands]
    context_doc = parse_json_stdout(results[8])
    alignment_doc = parse_json_stdout(results[9])
    regression_doc = parse_json_stdout(results[10])
    audit_doc = parse_json_stdout(results[1])
    report = {
        "package_version": manifest["version"],
        "validated_at": utc_now(),
        "status": "PASS" if all(r["exit_code"] == 0 for r in results) else "FAIL",
        "skill_package_audit": audit_doc.get("status", results[1]["status"]),
        "project_validator": parse_json_stdout(results[2]).get("status", results[2]["status"]),
        "narrative_audit": parse_json_stdout(results[3]).get("status", results[3]["status"]),
        "lexicon_audit": parse_json_stdout(results[4]).get("status", results[4]["status"]),
        "style_profile_audit": parse_json_stdout(results[5]).get("status", results[5]["status"]),
        "semantic_rubric_smoke": parse_json_stdout(results[6]).get("status", results[6]["status"]),
        "sample_calibration_smoke": parse_json_stdout(results[7]).get("status", results[7]["status"]),
        "context_compounding_smoke": context_doc.get("status", results[8]["status"]),
        "current_system_alignment": alignment_doc.get("status", results[9]["status"]),
        "regression": {
            "total": regression_doc.get("total", 0),
            "passed": regression_doc.get("passed", 0),
            "failed": regression_doc.get("failed", 0),
        },
        "manuscript_guard_smoke": parse_json_stdout(results[11]).get("status", results[11]["status"]),
        "engagement_contract_smoke": parse_json_stdout(results[16]).get("status", results[16]["status"]),
        "semantic_rubric_evidence_tests": parse_json_stdout(results[17]).get("status", results[17]["status"]),
        "workspace_project_audit": parse_json_stdout(results[18]).get("status", results[18]["status"]),
        "portable_export_tests": parse_json_stdout(results[19]).get("status", results[19]["status"]),
        "commands": results,
        "checks": [
            "Hyperagent-style export is rebuilt",
            "portable skill package audit passes",
            "project JSON fixture passes",
            "narrative audit fixture passes",
            "lexicon files validate and have no duplicate ids",
            "style profile structural audit runs on a representative fixture",
            "semantic 1-5 rubric scores validate against policy thresholds",
            "sample calibration derives term, voice, and im-not-ai alignment candidates without storing source prose",
            "context, evidence, state, review, recurrence, and promotion gates pass deterministic acceptance tests",
            "all prompts, policies, templates, collected data overlays, candidate resolutions, and freshness checks align",
            "regression suite passes",
            "manuscript guard wrapper PASS path is exercised with a stub guard",
            "all nine intent routes match current workflow steps and owners",
            "project/output context contracts and UTF-8 BOM compatibility pass",
            "workflow state transition and resumability invariants pass",
            "humanization evidence is bound to the exact manuscript hash",
            "character-first episode and scene engagement contracts pass deterministic fixtures",
            "semantic rubric scores require per-dimension scene or artifact evidence",
            "current projects validate while historical chunk descriptors remain evidence-only",
            "the single-JSON export rehydrates and executes dependency-bound validators in isolation",
            "input/output schemas and manifests are present",
            "script and asset checksums are present",
        ],
    }
    args.output.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 0 if report["status"] == "PASS" else 1


if __name__ == "__main__":
    sys.exit(main())

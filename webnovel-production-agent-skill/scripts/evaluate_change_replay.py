#!/usr/bin/env python3
"""Evaluate current and candidate behavior against human-approved replay cases."""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator

ROOT = Path(__file__).resolve().parents[1]


def evaluate(document: dict[str, Any]) -> dict[str, Any]:
    schema = json.loads((ROOT / "schemas" / "replay_evaluation.schema.json").read_text(encoding="utf-8"))
    schema_errors = sorted(Draft202012Validator(schema).iter_errors(document), key=lambda error: list(error.path))
    if schema_errors:
        return {"status": "FAIL", "errors": [{"code": "SCHEMA", "message": error.message} for error in schema_errors], "regressions": []}
    missing_artifacts = []
    for case in document["cases"]:
        for field in ("current_output", "candidate_output", "human_final"):
            path = Path(case[field])
            if not path.is_absolute():
                path = ROOT / path
            if not path.is_file():
                missing_artifacts.append(f"{case['case_id']}:{field}:{case[field]}")
    if missing_artifacts:
        return {"status": "FAIL", "errors": [{"code": "REPLAY_ARTIFACT_MISSING", "message": item} for item in missing_artifacts], "regressions": []}
    regressions = []
    current_values, candidate_values = [], []
    critical = set(document["critical_dimensions"])
    for case in document["cases"]:
        for dimension, comparison in case["scores"].items():
            current_values.append(comparison["current"]); candidate_values.append(comparison["candidate"])
            if dimension in critical and comparison["candidate"] < comparison["current"]:
                regressions.append(f"{case['case_id']}:{dimension}:candidate_below_current")
        if case["critical_failures"]["candidate"]:
            regressions.extend(f"{case['case_id']}:critical:{code}" for code in case["critical_failures"]["candidate"])
    current_average = sum(current_values) / len(current_values); candidate_average = sum(candidate_values) / len(candidate_values)
    if candidate_average < document["minimum_average"]:
        regressions.append("candidate_average_below_minimum")
    if candidate_average < current_average:
        regressions.append("candidate_average_below_current")
    return {"status": "FAIL" if regressions else "PASS", "errors": [{"code": "REGRESSION_DETECTED", "message": item} for item in regressions], "current_score": round(current_average, 3), "candidate_score": round(candidate_average, 3), "regressions": regressions, "case_count": len(document["cases"])}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__); parser.add_argument("evaluation", type=Path); parser.add_argument("--proposal", type=Path); parser.add_argument("--apply", action="store_true"); args = parser.parse_args()
    try:
        document = json.loads(args.evaluation.read_text(encoding="utf-8-sig")); output = evaluate(document)
        if args.apply:
            if args.proposal is None:
                raise ValueError("--proposal is required with --apply")
            proposal = json.loads(args.proposal.read_text(encoding="utf-8-sig")); proposal["replay"] = {"status": "pass" if output["status"] == "PASS" else "fail", "current_score": output.get("current_score"), "candidate_score": output.get("candidate_score"), "regressions": output.get("regressions", [])}; args.proposal.write_text(json.dumps(proposal, ensure_ascii=False, indent=2), encoding="utf-8")
    except (OSError, json.JSONDecodeError, ValueError) as exc:
        output = {"status": "FAIL", "errors": [{"code": "INPUT", "message": str(exc)}], "regressions": []}
    print(json.dumps(output, ensure_ascii=False, indent=2)); return 0 if output["status"] == "PASS" else 1


if __name__ == "__main__":
    sys.exit(main())

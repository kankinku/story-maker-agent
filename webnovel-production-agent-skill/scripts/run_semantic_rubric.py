#!/usr/bin/env python3
"""Validate human or judge supplied 1-5 semantic rubric scores."""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]

def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("scores", type=Path, help="JSON file with a scores object.")
    parser.add_argument("--policy", type=Path, default=ROOT / "config" / "evaluation_policy.json")
    parser.add_argument("--include-style", action="store_true", help="Require sample-style dimensions in addition to policy dimensions.")
    args = parser.parse_args()

    policy = load_json(args.policy)
    doc = load_json(args.scores)
    scores = doc.get("scores", {})
    issues: list[dict[str, Any]] = []

    required = list(policy.get("semantic_rubric", {}).get("dimensions", []))
    if args.include_style:
        style_dimensions = policy.get("sample_style_rubric", {}).get("dimensions", [])
        required.extend(dim for dim in style_dimensions if dim not in required)
    for dim in required:
        value = scores.get(dim)
        if not isinstance(value, int) or value < 1 or value > 5:
            issues.append({"severity": "error", "code": "RUBRIC_SCORE_MISSING_OR_RANGE", "dimension": dim, "message": "Score must be an integer from 1 to 5."})

    valid_values = [scores[dim] for dim in required if isinstance(scores.get(dim), int)]
    average = sum(valid_values) / len(valid_values) if valid_values else 0.0
    minimum_average = float(policy.get("semantic_rubric", {}).get("minimum_average", 4.0))
    if valid_values and average < minimum_average:
        issues.append({"severity": "error", "code": "RUBRIC_AVERAGE_LOW", "message": f"Average score {average:.2f} is below {minimum_average:.2f}."})

    critical_minimums = dict(policy.get("semantic_rubric", {}).get("critical_minimums", {}))
    if args.include_style:
        critical_minimums.update(policy.get("sample_style_rubric", {}).get("critical_minimums", {}))
    for dim, minimum in critical_minimums.items():
        value = scores.get(dim)
        if isinstance(value, int) and value < minimum:
            issues.append({"severity": "error", "code": "RUBRIC_CRITICAL_LOW", "dimension": dim, "message": f"{dim}={value} is below critical minimum {minimum}."})

    errors = [issue for issue in issues if issue["severity"] == "error"]
    result = {
        "status": "FAIL" if errors else "PASS",
        "average": round(average, 3),
        "checked_dimensions": required,
        "errors": errors,
        "policy": "This validates score shape and thresholds only; it does not replace human review.",
    }
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())

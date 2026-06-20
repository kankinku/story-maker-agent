#!/usr/bin/env python3
"""Audit episode manuscript length using non-space character counts."""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path


DEFAULT_MIN_NONSPACE = 3600


def count_nonspace(text: str) -> int:
    return sum(1 for char in text if not char.isspace())


def audit_path(path: Path, minimum: int) -> dict[str, object]:
    text = path.read_text(encoding="utf-8")
    nonspace = count_nonspace(text)
    passed = nonspace >= minimum
    return {
        "path": str(path),
        "characters": len(text),
        "nonspace_characters": nonspace,
        "minimum_nonspace_characters": minimum,
        "missing_nonspace_characters": max(0, minimum - nonspace),
        "passed": passed,
        "failure_code": "" if passed else "EPISODE_NONSPACE_UNDER_MINIMUM",
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("paths", nargs="+", type=Path, help="Episode TXT/MD files to audit.")
    parser.add_argument("--min-nonspace", type=int, default=DEFAULT_MIN_NONSPACE)
    parser.add_argument("--output", type=Path, help="Optional JSON report path.")
    args = parser.parse_args()

    results: list[dict[str, object]] = []
    for path in args.paths:
        if not path.exists():
            results.append({
                "path": str(path),
                "passed": False,
                "failure_code": "EPISODE_FILE_MISSING",
                "message": "Episode file does not exist.",
            })
            continue
        results.append(audit_path(path, args.min_nonspace))

    failed = [item for item in results if not item.get("passed")]
    report = {
        "status": "FAIL" if failed else "PASS",
        "minimum_nonspace_characters": args.min_nonspace,
        "counting_rule": "Unicode whitespace is excluded before counting.",
        "results": results,
        "metrics": {
            "checked": len(results),
            "failed": len(failed),
        },
    }

    rendered = json.dumps(report, ensure_ascii=False, indent=2)
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(rendered + "\n", encoding="utf-8")
    print(rendered)
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())

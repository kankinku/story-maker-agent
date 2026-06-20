#!/usr/bin/env python3
"""Test stub for ai_tell_guard.py."""
from __future__ import annotations

import argparse
import json
from pathlib import Path


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("manuscript", type=Path)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--fail-on-s1", action="store_true")
    args = parser.parse_args()
    args.output.write_text(
        json.dumps(
            {
                "status": "PASS",
                "s1_count": 0,
                "manuscript": str(args.manuscript),
                "fail_on_s1": args.fail_on_s1,
            },
            ensure_ascii=False,
            indent=2,
        ),
        encoding="utf-8",
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

#!/usr/bin/env python3
"""Resolve a supported request intent to the current workflow steps and owner."""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("intent")
    args = parser.parse_args()
    routes = json.loads((ROOT / "config" / "intent_routes.json").read_text(encoding="utf-8-sig"))["routes"]
    route = routes.get(args.intent)
    if route is None:
        print(json.dumps({"status": "FAIL", "errors": [{"code": "INTENT_UNSUPPORTED", "message": f"Unsupported intent: {args.intent}"}]}, ensure_ascii=False, indent=2))
        return 1
    print(json.dumps({"status": "PASS", "intent": args.intent, **route}, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())

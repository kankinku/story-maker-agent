#!/usr/bin/env python3
"""Populate sha256 checksums for scripts and assets in manifest.json."""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
PORTABLE_ASSET_GLOBS = (
    "config/*.json",
    "schemas/*.json",
    "templates/*.json",
    "prompts/*.md",
    "lexicons/*.json",
    "references/**/*.md",
    "sources/*.txt",
    "tests/**/*.json",
    "tests/**/*.txt",
    "tests/**/*.py",
)


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def normalize_asset(item: str | dict[str, Any]) -> dict[str, Any]:
    if isinstance(item, str):
        path = item
        doc: dict[str, Any] = {"path": path}
    else:
        doc = dict(item)
        path = doc["path"]
    doc["sha256"] = sha256(ROOT / path)
    return doc


def ensure_portable_assets(items: list[str | dict[str, Any]]) -> list[str | dict[str, Any]]:
    result = list(items)
    known = {item if isinstance(item, str) else item["path"] for item in result}
    discovered: set[str] = set()
    for pattern in PORTABLE_ASSET_GLOBS:
        discovered.update(path.relative_to(ROOT).as_posix() for path in ROOT.glob(pattern) if path.is_file())
    for path in sorted(discovered - known):
        result.append({"path": path})
    return result


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--manifest", type=Path, default=ROOT / "manifest.json")
    args = parser.parse_args()

    manifest = json.loads(args.manifest.read_text(encoding="utf-8"))
    manifest["assets"] = [normalize_asset(item) for item in ensure_portable_assets(manifest.get("assets", []))]
    scripts = []
    for item in manifest.get("scripts", []):
        doc = dict(item)
        doc["sha256"] = sha256(ROOT / doc["path"])
        scripts.append(doc)
    manifest["scripts"] = scripts
    args.manifest.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(args.manifest)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

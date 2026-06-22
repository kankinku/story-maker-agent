#!/usr/bin/env python3
"""Build a Hyperagent-style single JSON export from source files."""
from __future__ import annotations

import argparse
import base64
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PORTABLE_CORE_FILES = ("manifest.json", "metadata.json", "SKILL.md")


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def export_asset(path: Path) -> dict[str, str]:
    payload = path.read_bytes()
    result = {"path": path.relative_to(ROOT).as_posix(), "sha256": sha256(payload)}
    try:
        result.update({"encoding": "utf-8", "content": payload.decode("utf-8")})
    except UnicodeDecodeError:
        result.update({"encoding": "base64", "content": base64.b64encode(payload).decode("ascii")})
    return result


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=ROOT / "dist" / "webnovel-production-loop.skill.json")
    args = parser.parse_args()

    metadata = json.loads((ROOT / "metadata.json").read_text(encoding="utf-8"))
    manifest = json.loads((ROOT / "manifest.json").read_text(encoding="utf-8"))
    skill_body = (ROOT / "SKILL.md").read_text(encoding="utf-8")
    bundle_documents = []
    for name in metadata.get("bundleDocuments", []):
        path = ROOT / name
        if path.exists():
            bundle_documents.append(f"\n\n---\n\n# Bundled document: {name}\n\n" + path.read_text(encoding="utf-8"))
    documentation = skill_body + "".join(bundle_documents)

    scripts = []
    for path in sorted((ROOT / "scripts").glob("*.py")):
        scripts.append({
            "filename": path.name,
            "content": path.read_text(encoding="utf-8"),
            "description": metadata.get("scriptDescriptions", {}).get(path.name, "")
        })

    asset_paths = [item["path"] for item in manifest.get("assets", [])]
    asset_paths.extend(path for path in PORTABLE_CORE_FILES if path not in asset_paths)
    assets = [export_asset(ROOT / path) for path in asset_paths]

    export = {
        "version": 1,
        "type": "skill",
        "exportedAt": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
        "data": {
            "name": metadata["name"],
            "description": metadata["description"],
            "icon": None,
            "documentation": documentation,
            "tags": json.dumps(metadata["tags"], ensure_ascii=False),
            "whenToUse": metadata["whenToUse"],
            "authType": metadata.get("authType", "none"),
            "credentialSchema": metadata.get("credentialSchema"),
            "skillMdBody": documentation,
            "scripts": json.dumps(scripts, ensure_ascii=False),
            "assets": json.dumps(assets, ensure_ascii=False),
            "references": metadata.get("references")
        }
    }

    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(export, ensure_ascii=False, indent=2), encoding="utf-8")
    print(args.output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

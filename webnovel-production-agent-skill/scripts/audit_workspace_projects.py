#!/usr/bin/env python3
"""Audit registered current projects and classify historical chunk descriptors."""
from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]


def load(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8-sig"))


def run_json(command: list[str]) -> tuple[int, dict[str, Any]]:
    process = subprocess.run(command, capture_output=True, text=True, encoding="utf-8")
    try:
        payload = json.loads(process.stdout)
    except json.JSONDecodeError:
        payload = {"status": "FAIL", "raw": process.stdout, "stderr": process.stderr}
    return process.returncode, payload


def nonspace_count(path: Path) -> int:
    return len(re.sub(r"\s+", "", path.read_text(encoding="utf-8-sig"), flags=re.UNICODE))


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--project-root", type=Path, default=ROOT.parent)
    parser.add_argument("--registry", type=Path)
    args = parser.parse_args()
    project_root = args.project_root.resolve()
    registry_path = args.registry or project_root / "projects" / "project_registry.json"
    registry = load(registry_path)
    errors: list[dict[str, Any]] = []
    results: list[dict[str, Any]] = []
    registered_paths: set[str] = set()

    for entry in registry.get("projects", []):
        rel = entry.get("path", "")
        if rel in registered_paths:
            errors.append({"code": "PROJECT_REGISTRY_DUPLICATE", "path": rel})
            continue
        registered_paths.add(rel)
        path = project_root / rel
        if not path.exists():
            errors.append({"code": "REGISTERED_PROJECT_MISSING", "path": rel})
            continue
        classification = entry.get("classification")
        result: dict[str, Any] = {"project_id": entry.get("project_id"), "path": rel, "classification": classification}
        if classification == "current_project":
            validate_code, validate = run_json([sys.executable, str(ROOT / "scripts" / "validate_project.py"), str(path)])
            narrative_code, narrative = run_json([sys.executable, str(ROOT / "scripts" / "audit_narrative.py"), str(path)])
            result.update({"validate_status": validate.get("status"), "narrative_status": narrative.get("status")})
            if validate_code or narrative_code:
                errors.append({"code": "CURRENT_PROJECT_VALIDATION_FAILED", "path": rel, "validate": validate, "narrative": narrative})
        elif classification == "historical_chunk_descriptor":
            gate = entry.get("content_gate", {})
            files = sorted(project_root.glob(gate.get("episode_glob", "")))
            minimum = int(gate.get("minimum_nonspace_characters", 0))
            counts = {path.relative_to(project_root).as_posix(): nonspace_count(path) for path in files}
            failed = {path: count for path, count in counts.items() if count < minimum}
            result.update({
                "authority": entry.get("authority"),
                "content_status": gate.get("under_length_status") if failed else "PASS",
                "episode_count": len(files),
                "under_length_count": len(failed),
                "nonspace_range": [min(counts.values()), max(counts.values())] if counts else [],
            })
        else:
            errors.append({"code": "PROJECT_CLASSIFICATION_INVALID", "path": rel, "classification": classification})
        results.append(result)

    discovered = {path.relative_to(project_root).as_posix() for path in (project_root / "projects").glob("**/project.json")}
    for rel in sorted(discovered - registered_paths):
        errors.append({"code": "PROJECT_UNREGISTERED", "path": rel})
    for rel in sorted(registered_paths - discovered):
        errors.append({"code": "PROJECT_REGISTRY_PATH_NOT_DISCOVERED", "path": rel})

    output = {
        "status": "FAIL" if errors else "PASS",
        "errors": errors,
        "projects": results,
        "metrics": {
            "registered_project_count": len(registered_paths),
            "current_project_count": sum(item.get("classification") == "current_project" for item in results),
            "historical_descriptor_count": sum(item.get("classification") == "historical_chunk_descriptor" for item in results),
            "blocked_content_count": sum(item.get("content_status", "PASS") != "PASS" for item in results),
        },
    }
    print(json.dumps(output, ensure_ascii=False, indent=2))
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())

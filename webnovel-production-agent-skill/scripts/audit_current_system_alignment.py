#!/usr/bin/env python3
"""Audit that prompts, policies, templates, and collected data align with the current system."""
from __future__ import annotations

import argparse
import hashlib
import json
import sys
from datetime import date, datetime
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator, FormatChecker

ROOT = Path(__file__).resolve().parents[1]


def load(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8-sig"))


def issue(code: str, path: str, message: str) -> dict[str, str]:
    return {"code": code, "path": path, "message": message}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__); parser.add_argument("--project-root", type=Path, default=ROOT.parent); parser.add_argument("--as-of", default=date.today().isoformat()); args = parser.parse_args(); project_root = args.project_root.resolve()
    errors: list[dict[str, str]] = []
    prompts = sorted((ROOT / "prompts").glob("*.md"))
    for prompt in prompts:
        if "## Context-Compounding Contract" not in prompt.read_text(encoding="utf-8"):
            errors.append(issue("PROMPT_CONTEXT_CONTRACT_MISSING", prompt.relative_to(ROOT).as_posix(), "Every role prompt must declare the shared current contract."))
    registry = load(ROOT / "config" / "agent_registry.json")
    if len(prompts) != len(registry["roles"]):
        errors.append(issue("PROMPT_ROLE_COUNT_MISMATCH", "prompts", f"Found {len(prompts)} prompts for {len(registry['roles'])} roles."))
    sample_policy = load(ROOT / "config" / "agent_sample_evaluation_policy.json")
    integration = sample_policy.get("context_compounding_integration", {})
    if integration.get("policy") != "config/context_compounding_policy.json" or not integration.get("legacy_data_rule"):
        errors.append(issue("POLICY_CONTEXT_INTEGRATION_MISSING", "config/agent_sample_evaluation_policy.json", "Sample evaluation policy must bind current context and legacy-data rules."))
    sample_template = load(ROOT / "templates" / "agent_sample_loop_evaluation.json")
    for field in ["context_compounding", "human_review", "control_evidence"]:
        if field not in sample_template:
            errors.append(issue("TEMPLATE_CONTEXT_FIELD_MISSING", f"templates/agent_sample_loop_evaluation.json.{field}", "Current sample template field is required."))
    migration_path = project_root / "projects" / "sample_independent_loops" / "context_compounding_migration.json"
    if not migration_path.exists():
        errors.append(issue("MIGRATION_INDEX_MISSING", migration_path.as_posix(), "Collected legacy data requires a migration overlay."))
        migration = None
    else:
        migration = load(migration_path); schema = load(ROOT / "schemas" / "legacy_data_migration.schema.json")
        for error in Draft202012Validator(schema, format_checker=FormatChecker()).iter_errors(migration):
            errors.append(issue("MIGRATION_SCHEMA", migration_path.as_posix(), error.message))
        for artifact in migration.get("artifacts", []):
            path = project_root / artifact["path"]
            if not path.exists():
                errors.append(issue("MIGRATED_ARTIFACT_MISSING", artifact["path"], "Indexed artifact no longer exists.")); continue
            actual = "sha256:" + hashlib.sha256(path.read_bytes()).hexdigest()
            if actual != artifact["sha256"]:
                errors.append(issue("MIGRATED_ARTIFACT_DRIFT", artifact["path"], "Artifact changed after migration index generation."))
        if set(migration.get("candidate_resolutions", {})) != {f"CAND-{number:03d}" for number in range(1, 13)}:
            errors.append(issue("CANDIDATE_RESOLUTION_INCOMPLETE", migration_path.as_posix(), "All twelve collected candidates require a current resolution."))
    profiles = load(ROOT / "config" / "platform_profiles.json")
    sample_root = project_root / "projects" / "sample_independent_loops"
    current_overlay_count = 0
    for directory in sorted(path for path in sample_root.glob("sample_*") if path.is_dir()):
        expected = [directory / "context_plan.json", directory / "evidence_pack.json", directory / "component_versions.json", directory / "current_gate_status.json"]
        for path in expected:
            if not path.exists():
                errors.append(issue("CURRENT_SAMPLE_OVERLAY_MISSING", path.relative_to(project_root).as_posix(), "Every migrated sample requires current control artifacts."))
        if all(path.exists() for path in expected):
            current_overlay_count += 1
            evidence = load(directory / "evidence_pack.json"); gate = load(directory / "current_gate_status.json")
            source = next((item for item in evidence.get("evidence", []) if item.get("context_id") == "original-source"), None)
            if not source or source.get("status") != "missing" or source.get("required") is not True or gate.get("failure_code") != "CONTEXT_REQUIRED_MISSING" or gate.get("legacy_candidate_promotion_allowed") is not False:
                errors.append(issue("CURRENT_SAMPLE_GATE_INVALID", directory.relative_to(project_root).as_posix(), "Missing originals must block current execution and legacy promotion."))
    verified = datetime.fromisoformat(profiles["last_verified"]).date(); as_of = datetime.fromisoformat(args.as_of).date(); age = (as_of - verified).days
    if age > profiles["freshness_ttl_days"]:
        errors.append(issue("STALE_PLATFORM_FACT", "config/platform_profiles.json", f"Platform profile is {age} days old."))
    result = {"status": "FAIL" if errors else "PASS", "errors": errors, "metrics": {"role_prompt_count": len(prompts), "indexed_artifact_count": len(migration.get('artifacts', [])) if migration else 0, "candidate_resolution_count": len(migration.get('candidate_resolutions', {})) if migration else 0, "current_sample_overlay_count": current_overlay_count, "platform_profile_age_days": age}}
    print(json.dumps(result, ensure_ascii=False, indent=2)); return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())

#!/usr/bin/env python3
"""Build a non-destructive context-compounding overlay for collected legacy data."""
from __future__ import annotations

import argparse
import fnmatch
import hashlib
import json
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
SAMPLES = {
    "sample_01_muhan_regression": "무한회귀.txt",
    "sample_02_dimension_transfer": "차원이동.txt",
    "sample_03_transcendent_gallery": "초월자갤러리.txt",
    "sample_04_vampire_constraint": "흡혈귀.txt",
}


def sha(path: Path) -> str:
    return "sha256:" + hashlib.sha256(path.read_bytes()).hexdigest()


def classify(path: Path, patterns: dict[str, str]) -> str:
    for pattern, value in patterns.items():
        if fnmatch.fnmatch(path.name, pattern):
            return value
    return "historical_document"


def current_use(classification: str) -> str:
    if classification in {"historical_episodic_ledger", "historical_evaluation", "historical_candidate", "historical_structured_data", "historical_document"}:
        return "episodic_evidence"
    if classification == "derived_sample_evidence":
        return "derived_evidence"
    if classification == "historical_summary":
        return "historical_summary"
    if classification == "historical_rule_record":
        return "historical_rule_reference"
    if classification == "current_control_artifact":
        return "current_control"
    return "project_tooling"


def write_current_sample_overlays(project_root: Path, generated_at: str) -> None:
    root = project_root / "projects" / "sample_independent_loops"
    registry = json.loads((ROOT / "templates" / "component_version_registry.json").read_text(encoding="utf-8"))
    versions = {item["component_id"]: item["active_version"] for item in registry["components"]}
    for sample_id, source_name in SAMPLES.items():
        directory = root / sample_id
        if not directory.exists():
            continue
        plan = {"schema_version": "1.0.0", "project_id": sample_id, "task_id": f"migrate-{sample_id}", "intent": "incident", "required_context": [{"context_id": "original-source", "kind": "source_availability", "question": "Is the original source TXT available for reference evaluation?", "sources": [f"samples/{source_name}"], "freshness_hours": 0}], "optional_context": [{"context_id": "derived-element-pack", "kind": "style", "question": "Which derived functions remain usable as bounded hypotheses?", "sources": [f"projects/sample_independent_loops/{sample_id}/element_pack.json"], "freshness_hours": 0}], "created_at": generated_at}
        evidence = {"schema_version": "1.0.0", "project_id": sample_id, "task_id": f"migrate-{sample_id}", "story_bible_version": None, "evidence": [{"context_id": "original-source", "value": False, "source_id": f"samples/{source_name}", "source_type": "retrieval", "source_version": "missing", "authority": "primary", "retrieved_at": generated_at, "updated_at": generated_at, "freshness_hours": 0, "required": True, "status": "missing"}, {"context_id": "derived-element-pack", "value": "Derived functions may support bounded hypotheses only.", "source_id": f"projects/sample_independent_loops/{sample_id}/element_pack.json", "source_type": "retrieval", "source_version": "legacy-overlay-1.14.0", "authority": "secondary", "retrieved_at": generated_at, "updated_at": generated_at, "freshness_hours": 0, "required": False, "status": "resolved"}], "conflicts": [], "uncertainties": ["Original-reference fidelity cannot be scored until the source TXT is restored."], "generated_at": generated_at}
        gate = {"schema_version": "1.0.0", "package_version": "1.14.0", "sample_id": sample_id, "status": "BLOCKED", "failure_code": "CONTEXT_REQUIRED_MISSING", "blocking_context_id": "original-source", "next_action": "Restore the original TXT, rebuild the Evidence Pack, then rerun the current Inner Loop.", "legacy_candidate_promotion_allowed": False}
        for name, document in [("context_plan.json", plan), ("evidence_pack.json", evidence), ("component_versions.json", {"schema_version": "1.0.0", "components": versions}), ("current_gate_status.json", gate)]:
            (directory / name).write_text(json.dumps(document, ensure_ascii=False, indent=2), encoding="utf-8")


def build(project_root: Path, policy: dict[str, Any]) -> dict[str, Any]:
    paths: list[Path] = []
    for source in policy["source_roots"]:
        target = project_root / source
        if target.is_dir():
            paths.extend(path for path in target.rglob("*") if path.is_file() and path.name != "context_compounding_migration.json" and "__pycache__" not in path.parts and path.suffix != ".pyc")
        elif target.is_file():
            paths.append(target)
    unique = sorted(set(path.resolve() for path in paths))
    artifacts = []
    for path in unique:
        classification = classify(path, policy["classifications"])
        artifacts.append({"path": path.relative_to(project_root).as_posix(), "sha256": sha(path), "classification": classification, "authority": policy["authority_by_classification"][classification], "migration_status": "current_control_generated" if classification == "current_control_artifact" else "legacy_preserved_with_overlay", "current_use": current_use(classification)})
    immutable = sum(item["classification"] in {"historical_episodic_ledger", "historical_evaluation", "historical_candidate", "historical_rule_record"} for item in artifacts)
    derived = sum(item["classification"] == "derived_sample_evidence" for item in artifacts)
    return {"schema_version": "1.0.0", "migration_id": "context-compounding-legacy-data-1.14.0", "target_package_version": "1.14.0", "generated_at": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"), "principles": policy["principles"], "artifacts": artifacts, "candidate_resolutions": policy["candidate_resolutions"], "summary": {"artifact_count": len(artifacts), "immutable_record_count": immutable, "derived_evidence_count": derived, "canonical_artifact_count": 0, "unresolved_candidate_count": 0}}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__); parser.add_argument("--project-root", type=Path, default=ROOT.parent); parser.add_argument("--output", type=Path); args = parser.parse_args()
    project_root = args.project_root.resolve(); policy = json.loads((ROOT / "config" / "legacy_data_migration_policy.json").read_text(encoding="utf-8")); generated_at = datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"); write_current_sample_overlays(project_root, generated_at); document = build(project_root, policy); document["generated_at"] = generated_at
    output = args.output or project_root / "projects" / "sample_independent_loops" / "context_compounding_migration.json"; output.parent.mkdir(parents=True, exist_ok=True); output.write_text(json.dumps(document, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps({"status": "PASS", "output": str(output), "summary": document["summary"]}, ensure_ascii=False, indent=2)); return 0


if __name__ == "__main__":
    sys.exit(main())

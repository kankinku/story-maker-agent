#!/usr/bin/env python3
"""Run deterministic context-compounding acceptance tests."""
from __future__ import annotations

import copy
import importlib.util
import json
import subprocess
import sys
import tempfile
from argparse import Namespace
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Callable

ROOT = Path(__file__).resolve().parents[1]


def load_module(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Cannot load {path}")
    module = importlib.util.module_from_spec(spec); spec.loader.exec_module(module); return module


AUDIT = load_module(ROOT / "scripts" / "audit_context_compounding.py", "context_audit")
DIFF = load_module(ROOT / "scripts" / "analyze_review_diff.py", "review_diff")
REPLAY = load_module(ROOT / "scripts" / "evaluate_change_replay.py", "change_replay")


def template(name: str) -> dict[str, Any]:
    return json.loads((ROOT / "templates" / name).read_text(encoding="utf-8"))


def codes(output: dict[str, Any]) -> set[str]:
    return {item["code"] for item in output.get("errors", [])}


def main() -> int:
    artifact_workspace = tempfile.TemporaryDirectory()
    artifact_root = Path(artifact_workspace.name)
    fixed_now = datetime(2026, 6, 20, tzinfo=timezone.utc)
    plan, evidence = template("context_plan.json"), template("evidence_pack.json")
    characters, relationships = template("character_state.json"), template("relationship_state.json")
    roleplay, delta = template("roleplay_result.json"), template("episode_memory_delta.json")
    review, proposal, registry = template("review_packet.json"), template("change_proposal.json"), template("component_version_registry.json")
    review_draft, review_final = artifact_root / "review.draft.txt", artifact_root / "review.final.txt"
    review_draft.write_text("draft", encoding="utf-8"); review_final.write_text("approved final", encoding="utf-8")
    review["draft_path"] = str(review_draft); review["final_path"] = str(review_final)
    replay = template("replay_evaluation.json")
    replay_current, replay_candidate, replay_final = artifact_root / "replay.current.txt", artifact_root / "replay.candidate.txt", artifact_root / "replay.final.txt"
    replay_current.write_text("current", encoding="utf-8"); replay_candidate.write_text("candidate", encoding="utf-8"); replay_final.write_text("human final", encoding="utf-8")
    replay["cases"][0]["current_output"] = str(replay_current); replay["cases"][0]["candidate_output"] = str(replay_candidate); replay["cases"][0]["human_final"] = str(replay_final)
    cases: list[tuple[str, Callable[[], dict[str, Any]], str, set[str]]] = []
    cases.append(("valid_inner", lambda: AUDIT.audit_inner(plan, evidence, fixed_now), "PASS", set()))
    duplicate_evidence = copy.deepcopy(evidence); duplicate_evidence["evidence"].append(copy.deepcopy(duplicate_evidence["evidence"][0])); duplicate_evidence["evidence"][-1]["value"] = "conflicting duplicate"
    cases.append(("duplicate_evidence_ids", lambda: AUDIT.audit_inner(plan, duplicate_evidence, fixed_now), "FAIL", {"EVIDENCE_ID_DUPLICATE"}))
    missing = copy.deepcopy(evidence); missing["evidence"][0]["status"] = "missing"
    cases.append(("missing_required_context", lambda: AUDIT.audit_inner(plan, missing, fixed_now), "FAIL", {"CONTEXT_REQUIRED_MISSING"}))
    conflicted = copy.deepcopy(evidence); conflicted["conflicts"] = [{"field": "character.location", "source_ids": ["a", "b"], "status": "unresolved", "action": "human_review_required"}]
    cases.append(("unresolved_conflict", lambda: AUDIT.audit_inner(plan, conflicted, fixed_now), "FAIL", {"EVIDENCE_CONFLICT_UNRESOLVED"}))
    stale = copy.deepcopy(evidence); stale["evidence"][1]["updated_at"] = "2026-06-18T00:00:00Z"
    cases.append(("stale_context", lambda: AUDIT.audit_inner(plan, stale, fixed_now), "FAIL", {"STALE_CONTEXT"}))
    cases.append(("valid_three_character_state", lambda: AUDIT.audit_state(characters, relationships, roleplay, delta), "PASS", set()))
    duplicate_characters = copy.deepcopy(characters); duplicate_characters["characters"].append(copy.deepcopy(duplicate_characters["characters"][0]))
    duplicate_relationships = copy.deepcopy(relationships); duplicate_relationships["relationships"].append(copy.deepcopy(duplicate_relationships["relationships"][0]))
    duplicate_roleplay = copy.deepcopy(roleplay); duplicate_roleplay["participants"].append(copy.deepcopy(duplicate_roleplay["participants"][0]))
    cases.append(("duplicate_state_ids", lambda: AUDIT.audit_state(duplicate_characters, duplicate_relationships, duplicate_roleplay, delta), "FAIL", {"STATE_ID_DUPLICATE"}))
    leaked_roleplay = copy.deepcopy(roleplay); leaked_roleplay["participants"][1]["known_facts"].append(characters["characters"][0]["secrets"][0])
    cases.append(("roleplay_blocks_unowned_secret_knowledge", lambda: AUDIT.audit_state(characters, relationships, leaked_roleplay, delta), "FAIL", {"CHARACTER_KNOWLEDGE_LEAK"}))
    drift = copy.deepcopy(delta); drift["changes"][0]["before"] = []
    cases.append(("character_state_drift", lambda: AUDIT.audit_state(characters, relationships, roleplay, drift), "FAIL", {"CHARACTER_STATE_DRIFT"}))
    unapproved = copy.deepcopy(delta); unapproved["human_approval"] = {"status": "pending", "approval_id": "", "approved_by": "", "approved_at": None}
    cases.append(("unapproved_delta", lambda: AUDIT.audit_state(characters, relationships, roleplay, unapproved), "FAIL", {"CANON_DELTA_UNAPPROVED"}))
    cases.append(("valid_review_pair", lambda: AUDIT.audit_review(review), "PASS", set()))
    no_pair = copy.deepcopy(review); no_pair["final_path"] = no_pair["draft_path"]
    cases.append(("missing_review_pair", lambda: AUDIT.audit_review(no_pair), "FAIL", {"REVIEW_PAIR_MISSING"}))
    nonexistent_pair = copy.deepcopy(review); nonexistent_pair["draft_path"] = str(artifact_root / "missing.draft.txt")
    cases.append(("nonexistent_review_pair", lambda: AUDIT.audit_review(nonexistent_pair), "FAIL", {"REVIEW_PAIR_MISSING"}))
    cases.append(("proposed_change_is_reviewable", lambda: AUDIT.audit_control(proposal, registry), "PASS", set()))
    unsafe = copy.deepcopy(proposal); unsafe["status"] = "candidate"
    cases.append(("candidate_without_approval_or_replay", lambda: AUDIT.audit_control(unsafe, registry), "FAIL", {"PROMOTION_APPROVAL_MISSING", "REGRESSION_DETECTED"}))
    cases.append(("offline_replay_passes", lambda: REPLAY.evaluate(replay), "PASS", set()))
    replay_missing = copy.deepcopy(replay); replay_missing["cases"][0]["human_final"] = str(artifact_root / "missing.final.txt")
    cases.append(("offline_replay_requires_real_artifacts", lambda: REPLAY.evaluate(replay_missing), "FAIL", {"REPLAY_ARTIFACT_MISSING"}))
    replay_regression = copy.deepcopy(replay); replay_regression["cases"][0]["scores"]["canon_fidelity"]["candidate"] = 2.0
    cases.append(("offline_replay_blocks_regression", lambda: REPLAY.evaluate(replay_regression), "FAIL", {"REGRESSION_DETECTED"}))
    project_root = ROOT.parent
    legacy_semantics = []
    for sample_id in ["sample_01_muhan_regression", "sample_02_dimension_transfer", "sample_03_transcendent_gallery", "sample_04_vampire_constraint"]:
        sample_dir = project_root / "projects" / "sample_independent_loops" / sample_id
        sample_plan = json.loads((sample_dir / "context_plan.json").read_text(encoding="utf-8")); sample_evidence = json.loads((sample_dir / "evidence_pack.json").read_text(encoding="utf-8"))
        cases.append((f"{sample_id}_blocks_without_original", lambda plan=sample_plan, evidence=sample_evidence: AUDIT.audit_inner(plan, evidence, fixed_now), "FAIL", {"CONTEXT_REQUIRED_MISSING"}))
        legacy_semantics.append(sample_plan["required_context"][0]["kind"] == "source_availability" and sample_evidence["story_bible_version"] is None)
    cases.append(("legacy_source_availability_and_no_canon_are_explicit", lambda: AUDIT.result([] if all(legacy_semantics) else [AUDIT.finding("LEGACY_SEMANTICS", "Legacy source availability or absent canon is mislabeled.")]), "PASS", set()))
    migration = json.loads((project_root / "projects" / "sample_independent_loops" / "context_compounding_migration.json").read_text(encoding="utf-8"))
    cases.append(("legacy_migration_schema_valid", lambda: AUDIT.result(AUDIT.schema_errors("legacy_data_migration", migration)), "PASS", set()))

    results = []
    for name, run, expected_status, expected_codes in cases:
        output = run(); passed = output["status"] == expected_status and expected_codes.issubset(codes(output))
        results.append({"case": name, "passed": passed, "expected_status": expected_status, "actual_status": output["status"], "expected_codes": sorted(expected_codes), "actual_codes": sorted(codes(output))})

    with tempfile.TemporaryDirectory() as directory:
        root = Path(directory)
        base = template("review_diff.json")
        for count in range(2):
            item = copy.deepcopy(base); item["diff_id"] = f"d{count}"; item["review_id"] = f"r{count}"; item["reviewed_at"] = f"2026-06-{18 + count:02d}T00:00:00Z"
            (root / f"{count}.json").write_text(json.dumps(item), encoding="utf-8")
        two = DIFF.aggregate(Namespace(input_dir=root, output=None))
        two_passed = two["metrics"]["promotable_candidate_count"] == 0
        item = copy.deepcopy(base); item["diff_id"] = "d2"; item["review_id"] = "r2"; item["reviewed_at"] = "2026-06-20T00:00:00Z"
        (root / "2.json").write_text(json.dumps(item), encoding="utf-8")
        three = DIFF.aggregate(Namespace(input_dir=root, output=None))
        three_passed = three["metrics"]["promotable_candidate_count"] == 1 and three["candidates"][0]["count"] == 3
        results.extend([
            {"case": "two_reviews_do_not_promote", "passed": two_passed, "expected_status": "PASS", "actual_status": "PASS" if two_passed else "FAIL", "expected_codes": [], "actual_codes": []},
            {"case": "three_same_scope_reviews_promote", "passed": three_passed, "expected_status": "PASS", "actual_status": "PASS" if three_passed else "FAIL", "expected_codes": [], "actual_codes": []},
        ])

    with tempfile.TemporaryDirectory() as directory:
        root = Path(directory)
        duplicate = template("review_diff.json")
        duplicate["review_id"] = "same-review"
        for count in range(3):
            item = copy.deepcopy(duplicate); item["diff_id"] = f"duplicate-{count}"
            (root / f"{count}.json").write_text(json.dumps(item), encoding="utf-8")
        duplicate_result = DIFF.aggregate(Namespace(input_dir=root, output=None))
        duplicate_blocked = duplicate_result["metrics"]["completed_reviews_considered"] == 1 and duplicate_result["metrics"]["promotable_candidate_count"] == 0
        results.append({"case": "duplicate_review_ids_do_not_promote", "passed": duplicate_blocked, "expected_status": "PASS", "actual_status": "PASS" if duplicate_blocked else "FAIL", "expected_codes": [], "actual_codes": []})

    with tempfile.TemporaryDirectory() as directory:
        root = Path(directory); proposal_path = root / "proposal.json"; registry_path = root / "registry.json"
        transition_proposal = copy.deepcopy(proposal)
        transition_proposal["approvals"]["candidate"] = {"status": "approved", "approval_id": "candidate-ok", "approved_by": "author"}
        transition_proposal["replay"] = {"status": "pass", "current_score": 4.0, "candidate_score": 4.2, "regressions": []}
        proposal_path.write_text(json.dumps(transition_proposal), encoding="utf-8"); registry_path.write_text(json.dumps(registry), encoding="utf-8")
        base = [sys.executable, str(ROOT / "scripts" / "manage_component_versions.py")]
        common = ["--registry", str(registry_path), "--proposal", str(proposal_path), "--component-id", "context-router"]
        candidate_run = subprocess.run(base + ["candidate"] + common + ["--candidate-version", "1.3.0"], capture_output=True, text=True)
        canary_run = subprocess.run(base + ["canary"] + common, capture_output=True, text=True)
        transition_proposal = json.loads(proposal_path.read_text(encoding="utf-8")); transition_proposal["canary"] = {"task_limit": 1, "completed_tasks": 1, "status": "pass"}; transition_proposal["approvals"]["promotion"] = {"status": "approved", "approval_id": "promotion-ok", "approved_by": "author"}; proposal_path.write_text(json.dumps(transition_proposal), encoding="utf-8")
        promote_run = subprocess.run(base + ["promote"] + common, capture_output=True, text=True)
        transition_proposal = json.loads(proposal_path.read_text(encoding="utf-8")); transition_proposal["canary"]["status"] = "fail"; proposal_path.write_text(json.dumps(transition_proposal), encoding="utf-8")
        rollback_run = subprocess.run(base + ["rollback"] + common, capture_output=True, text=True)
        final_registry = json.loads(registry_path.read_text(encoding="utf-8")); final_component = next(item for item in final_registry["components"] if item["component_id"] == "context-router")
        transition_passed = all(run.returncode == 0 for run in [candidate_run, canary_run, promote_run, rollback_run]) and final_component["active_version"] == "1.2.0" and final_component["status"] == "rolled_back"
        results.append({"case": "candidate_canary_promote_rollback", "passed": transition_passed, "expected_status": "PASS", "actual_status": "PASS" if transition_passed else "FAIL", "expected_codes": [], "actual_codes": []})

    with tempfile.TemporaryDirectory() as directory:
        root = Path(directory); proposal_path = root / "proposal.json"; registry_path = root / "registry.json"
        proposal_path.write_text(json.dumps(proposal), encoding="utf-8"); registry_path.write_text(json.dumps(registry), encoding="utf-8")
        rollback_run = subprocess.run([sys.executable, str(ROOT / "scripts" / "manage_component_versions.py"), "rollback", "--registry", str(registry_path), "--proposal", str(proposal_path), "--component-id", "context-router"], capture_output=True, text=True, encoding="utf-8")
        rollback_output = json.loads(rollback_run.stdout)
        rollback_blocked = rollback_run.returncode != 0 and "ROLLBACK_REASON_MISSING" in codes(rollback_output)
        results.append({"case": "rollback_requires_regression_evidence", "passed": rollback_blocked, "expected_status": "FAIL", "actual_status": rollback_output["status"], "expected_codes": ["ROLLBACK_REASON_MISSING"], "actual_codes": sorted(codes(rollback_output))})

    with tempfile.TemporaryDirectory() as directory:
        root = Path(directory)
        character_path, relationship_path, delta_path = root / "characters.json", root / "relationships.json", root / "delta.json"
        character_path.write_text(json.dumps(characters), encoding="utf-8")
        relationship_path.write_text(json.dumps(relationships), encoding="utf-8")
        canon_delta = copy.deepcopy(delta)
        canon_delta["changes"] = [{"target_type": "canon_decision", "target_id": "canon-001", "field": "value", "before": "old", "after": "new", "source_id": "episode:001"}]
        delta_path.write_text(json.dumps(canon_delta), encoding="utf-8")
        commit_run = subprocess.run(
            [sys.executable, str(ROOT / "scripts" / "commit_episode_state.py"), "--character-state", str(character_path), "--relationship-state", str(relationship_path), "--delta", str(delta_path)],
            capture_output=True, text=True, encoding="utf-8",
        )
        commit_output = json.loads(commit_run.stdout)
        unchanged = json.loads(character_path.read_text(encoding="utf-8"))["state_version"] == characters["state_version"]
        canon_blocked = commit_run.returncode != 0 and "CANON_TARGET_UNSUPPORTED" in codes(commit_output) and unchanged
        results.append({"case": "canon_delta_cannot_be_silently_dropped", "passed": canon_blocked, "expected_status": "FAIL", "actual_status": commit_output["status"], "expected_codes": ["CANON_TARGET_UNSUPPORTED"], "actual_codes": sorted(codes(commit_output))})

    with tempfile.TemporaryDirectory() as directory:
        root = Path(directory)
        character_path, relationship_path, delta_path = root / "characters.json", root / "relationships.json", root / "delta.json"
        character_path.write_text(json.dumps(characters), encoding="utf-8"); relationship_path.write_text(json.dumps(relationships), encoding="utf-8"); delta_path.write_text(json.dumps(delta), encoding="utf-8")
        commit_run = subprocess.run(
            [sys.executable, str(ROOT / "scripts" / "commit_episode_state.py"), "--character-state", str(character_path), "--relationship-state", str(relationship_path), "--delta", str(delta_path)],
            capture_output=True, text=True, encoding="utf-8",
        )
        committed_characters = json.loads(character_path.read_text(encoding="utf-8")); committed_relationships = json.loads(relationship_path.read_text(encoding="utf-8"))
        inspector = next(item for item in committed_characters["characters"] if item["character_id"] == "inspector")
        relation = next(item for item in committed_relationships["relationships"] if item["relationship_id"] == "protagonist-inspector")
        evidence_updated = commit_run.returncode == 0 and inspector["last_evidence"] == {"episode": 1, "source_id": "episode:001"} and relation["last_evidence"] == {"episode": 1, "source_id": "episode:001"}
        results.append({"case": "state_commit_updates_last_evidence", "passed": evidence_updated, "expected_status": "PASS", "actual_status": "PASS" if evidence_updated else "FAIL", "expected_codes": [], "actual_codes": []})

    with tempfile.TemporaryDirectory() as directory:
        root = Path(directory); character_path, relationship_path, delta_path = root / "characters.json", root / "relationships.json", root / "delta.json"
        character_path.write_text(json.dumps(characters), encoding="utf-8"); relationship_path.write_text(json.dumps(relationships), encoding="utf-8")
        malformed_delta = copy.deepcopy(delta); malformed_delta.pop("changes")
        delta_path.write_text(json.dumps(malformed_delta), encoding="utf-8")
        malformed_run = subprocess.run([sys.executable, str(ROOT / "scripts" / "commit_episode_state.py"), "--character-state", str(character_path), "--relationship-state", str(relationship_path), "--delta", str(delta_path)], capture_output=True, text=True, encoding="utf-8")
        malformed_output = json.loads(malformed_run.stdout)
        schema_blocked = malformed_run.returncode != 0 and "SCHEMA" in codes(malformed_output)
        results.append({"case": "commit_validates_input_schema", "passed": schema_blocked, "expected_status": "FAIL", "actual_status": malformed_output["status"], "expected_codes": ["SCHEMA"], "actual_codes": sorted(codes(malformed_output))})

    legacy_root = project_root / "projects" / "sample_independent_loops"
    manifest_hash_before = (legacy_root / "run_manifest.json").read_bytes()
    legacy_runs = [subprocess.run([sys.executable, str(legacy_root / script)], capture_output=True, text=True, encoding="utf-8") for script in ["run_100_task_batch.py", "run_sequential_100_improvements.py"]]
    legacy_blocked = all(run.returncode == 0 and json.loads(run.stdout).get("code") == "LEGACY_RUNNER_READ_ONLY" for run in legacy_runs) and manifest_hash_before == (legacy_root / "run_manifest.json").read_bytes()
    results.append({"case": "legacy_runners_are_read_only", "passed": legacy_blocked, "expected_status": "PASS", "actual_status": "PASS" if legacy_blocked else "FAIL", "expected_codes": [], "actual_codes": []})

    failed = sum(not item["passed"] for item in results)
    output = {"status": "FAIL" if failed else "PASS", "total": len(results), "passed": len(results) - failed, "failed": failed, "results": results}
    print(json.dumps(output, ensure_ascii=False, indent=2)); artifact_workspace.cleanup(); return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())

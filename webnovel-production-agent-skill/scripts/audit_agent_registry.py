#!/usr/bin/env python3
"""Audit agent registry, duplicate routing authority, and sample-loop policy."""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8-sig"))


def add_issue(issues: list[dict[str, str]], severity: str, code: str, path: str, message: str) -> None:
    issues.append({"severity": severity, "code": code, "path": path, "message": message})


def resolve_package_path(rel: str) -> Path:
    return (ROOT / rel).resolve()


def resolve_project_path(rel: str, project_root: Path) -> Path:
    candidate = Path(rel)
    if candidate.is_absolute():
        return candidate
    if rel.startswith("../"):
        return (ROOT / rel).resolve()
    return (project_root / rel).resolve()


def audit(project_root: Path) -> list[dict[str, str]]:
    issues: list[dict[str, str]] = []
    registry_path = ROOT / "config" / "agent_registry.json"
    policy_path = ROOT / "config" / "agent_sample_evaluation_policy.json"
    system_improvement_policy_path = ROOT / "config" / "system_improvement_policy.json"
    source_chunk_policy_path = ROOT / "config" / "source_chunk_policy.json"
    manuscript_length_policy_path = ROOT / "config" / "manuscript_length_policy.json"
    context_compounding_policy_path = ROOT / "config" / "context_compounding_policy.json"
    improvement_template_path = ROOT / "templates" / "system_improvement_point.json"
    source_chunk_template_path = ROOT / "templates" / "source_chunk_cycle.json"
    adapter_path = ROOT / "prompts" / "orchestrator.md"

    for path in [registry_path, policy_path, system_improvement_policy_path, source_chunk_policy_path, manuscript_length_policy_path, context_compounding_policy_path, improvement_template_path, source_chunk_template_path, adapter_path]:
        if not path.exists():
            add_issue(issues, "error", "MISSING_FILE", str(path.relative_to(ROOT)), "Required agent evaluation file is missing.")
    if issues:
        return issues

    registry = load_json(registry_path)
    policy = load_json(policy_path)
    system_improvement_policy = load_json(system_improvement_policy_path)
    source_chunk_policy = load_json(source_chunk_policy_path)
    manuscript_length_policy = load_json(manuscript_length_policy_path)
    context_compounding_policy = load_json(context_compounding_policy_path)
    improvement_template = load_json(improvement_template_path)
    source_chunk_template = load_json(source_chunk_template_path)
    roles = registry.get("roles", [])
    agents = policy.get("agents", {})
    sample_group = policy.get("sample_group", {})

    inner_policy = context_compounding_policy.get("inner_loop", {})
    outer_policy = context_compounding_policy.get("outer_loop", {})
    control_policy = context_compounding_policy.get("control_loop", {})
    if inner_policy.get("maximum_writer_candidates") != 2 or inner_policy.get("paragraph_level_candidate_merge_allowed") is not False:
        add_issue(issues, "error", "WRITER_CANDIDATE_POLICY", "config/context_compounding_policy.json.inner_loop", "Writer candidates must be limited to two and paragraph merging must be disabled.")
    if outer_policy.get("review_window") != 10 or outer_policy.get("minimum_same_scope_occurrences") != 3 or outer_policy.get("maximum_proposals_per_run") != 3:
        add_issue(issues, "error", "OUTER_LOOP_THRESHOLD", "config/context_compounding_policy.json.outer_loop", "Outer Loop must use latest 10 reviews, 3 same-scope occurrences, and at most 3 proposals.")
    if control_policy.get("automatic_promotion_allowed") is not False or control_policy.get("canary_task_count") != 1 or not control_policy.get("human_approval_required_for_candidate") or not control_policy.get("human_approval_required_for_promotion"):
        add_issue(issues, "error", "CONTROL_LOOP_APPROVAL", "config/context_compounding_policy.json.control_loop", "Control Loop must prohibit automatic promotion and require two approvals around one canary task.")
    for path in ["scripts/audit_context_compounding.py", "scripts/analyze_review_diff.py", "scripts/commit_episode_state.py", "scripts/evaluate_change_replay.py", "scripts/manage_component_versions.py", "scripts/run_context_compounding_tests.py", "scripts/migrate_legacy_context_data.py", "scripts/audit_current_system_alignment.py"]:
        if not (ROOT / path).exists():
            add_issue(issues, "error", "CONTEXT_SCRIPT_MISSING", path, "Context-compounding runtime script is required.")

    if not isinstance(roles, list) or len(roles) != 13:
        add_issue(issues, "error", "ROLE_COUNT", "config/agent_registry.json.roles", "Registry must define exactly 13 roles.")

    role_ids = [role.get("id") for role in roles if isinstance(role, dict)]
    duplicate_ids = sorted({role_id for role_id in role_ids if role_ids.count(role_id) > 1})
    if duplicate_ids:
        add_issue(issues, "error", "ROLE_ID_DUPLICATE", "config/agent_registry.json.roles", ", ".join(duplicate_ids))

    role_numbers = [role.get("number") for role in roles if isinstance(role, dict)]
    duplicate_numbers = sorted({number for number in role_numbers if role_numbers.count(number) > 1})
    if duplicate_numbers:
        add_issue(issues, "error", "ROLE_NUMBER_DUPLICATE", "config/agent_registry.json.roles", ", ".join(map(str, duplicate_numbers)))

    if sorted(role_numbers) != list(range(1, 14)):
        add_issue(issues, "error", "ROLE_NUMBER_SEQUENCE", "config/agent_registry.json.roles", "Role numbers must be 1 through 13.")

    canonical = registry.get("canonical_runtime_agent", {})
    if canonical.get("id") != "webnovel_orchestrator":
        add_issue(issues, "error", "CANONICAL_AGENT_ID", "config/agent_registry.json.canonical_runtime_agent", "Canonical runtime agent must be webnovel_orchestrator.")
    canonical_path = resolve_project_path(str(canonical.get("path", "")), project_root)
    if not canonical_path.exists():
        add_issue(issues, "error", "CANONICAL_AGENT_MISSING", str(canonical.get("path", "")), "Canonical runtime agent file does not exist.")

    runtime_owners = [role for role in roles if role.get("owns_runtime_routing") is True]
    if len(runtime_owners) != 1:
        add_issue(issues, "error", "ROUTING_OWNER_COUNT", "config/agent_registry.json.roles", "Exactly one role may own runtime routing.")
    elif runtime_owners[0].get("id") != "orchestrator":
        add_issue(issues, "error", "ROUTING_OWNER_ROLE", "config/agent_registry.json.roles", "Only the orchestrator role may own runtime routing.")

    duplicate_resolution = registry.get("duplicate_resolution", {})
    if duplicate_resolution.get("package_orchestrator_prompt") != "adapter_only":
        add_issue(issues, "error", "ORCHESTRATOR_ADAPTER_RULE", "config/agent_registry.json.duplicate_resolution", "Package orchestrator prompt must be adapter_only.")

    adapter_text = adapter_path.read_text(encoding="utf-8")
    if "adapter, not an independent runtime router" not in adapter_text:
        add_issue(issues, "error", "ADAPTER_TEXT_MISSING", "prompts/orchestrator.md", "Orchestrator prompt must state it is not an independent runtime router.")

    for role in roles:
        if not isinstance(role, dict):
            add_issue(issues, "error", "ROLE_SHAPE", "config/agent_registry.json.roles", "Each role must be an object.")
            continue
        prompt_path = role.get("prompt_path")
        if not prompt_path or not resolve_package_path(str(prompt_path)).exists():
            add_issue(issues, "error", "PROMPT_MISSING", str(prompt_path), f"Prompt for {role.get('id')} does not exist.")

    rights_roles = [role for role in roles if role.get("id") == "rights_reviewer" or role.get("number") == 10]
    if len(rights_roles) != 1:
        add_issue(issues, "error", "RIGHTS_ROLE_SHAPE", "config/agent_registry.json.roles", "There must be exactly one role 10 rights_reviewer entry.")
    else:
        rights = rights_roles[0]
        if rights.get("id") != "rights_reviewer" or rights.get("number") != 10:
            add_issue(issues, "error", "RIGHTS_ROLE_NUMBER", "config/agent_registry.json.roles", "Role 10 must be rights_reviewer.")
        if rights.get("sample_loop_evaluation") != "excluded":
            add_issue(issues, "error", "RIGHTS_INCLUDED", "config/agent_registry.json.roles[10]", "Role 10 must be excluded from sample-loop evaluation.")

    excluded_ids = {item.get("agent_id") for item in policy.get("excluded_roles", []) if isinstance(item, dict)}
    if "rights_reviewer" not in excluded_ids:
        add_issue(issues, "error", "RIGHTS_POLICY_EXCLUSION_MISSING", "config/agent_sample_evaluation_policy.json.excluded_roles", "Policy must exclude rights_reviewer.")
    if "rights_reviewer" in agents:
        add_issue(issues, "error", "RIGHTS_POLICY_INCLUDED", "config/agent_sample_evaluation_policy.json.agents", "Policy agents must not include rights_reviewer.")
    required_context_roles = {"context_evidence_planner", "character_state_keeper", "review_diff_analyst"}
    missing_context_exclusions = sorted(required_context_roles - excluded_ids)
    if missing_context_exclusions:
        add_issue(issues, "error", "CONTEXT_ROLE_EXCLUSION_MISSING", "config/agent_sample_evaluation_policy.json.excluded_roles", ", ".join(missing_context_exclusions))

    if sample_group.get("evaluation_mode") != "independent_per_sample_parallel":
        add_issue(issues, "error", "SAMPLE_EVALUATION_MODE", "config/agent_sample_evaluation_policy.json.sample_group.evaluation_mode", "Sample-loop evaluation must run as independent_per_sample_parallel.")
    sample_files = sample_group.get("parallel_sample_files", [])
    if not isinstance(sample_files, list) or len(sample_files) != 4:
        add_issue(issues, "error", "PARALLEL_SAMPLE_COUNT", "config/agent_sample_evaluation_policy.json.sample_group.parallel_sample_files", "Exactly four independent sample files must be listed.")
    job_workflow = policy.get("per_sample_job_workflow", [])
    required_stages = [
        "element_extract",
        "agent_recreation",
        "original_reference_evaluation_without_plagiarism_check",
        "queue_improvement_point",
        "close_task",
    ]
    if job_workflow != required_stages:
        add_issue(issues, "error", "PER_SAMPLE_WORKFLOW", "config/agent_sample_evaluation_policy.json.per_sample_job_workflow", "Per-sample workflow must be element extraction -> recreation -> original-reference evaluation without plagiarism check -> queue improvement point -> close task.")

    source_chunk_cycle = policy.get("source_chunk_cycle", {})
    if source_chunk_cycle.get("policy") != "config/source_chunk_policy.json":
        add_issue(issues, "error", "SOURCE_CHUNK_POLICY_REF", "config/agent_sample_evaluation_policy.json.source_chunk_cycle.policy", "Source chunk cycle must reference config/source_chunk_policy.json.")
    if source_chunk_cycle.get("template") != "templates/source_chunk_cycle.json":
        add_issue(issues, "error", "SOURCE_CHUNK_TEMPLATE_REF", "config/agent_sample_evaluation_policy.json.source_chunk_cycle.template", "Source chunk cycle must reference templates/source_chunk_cycle.json.")
    if source_chunk_cycle.get("overall_cycle_stage") != 1:
        add_issue(issues, "error", "SOURCE_CHUNK_STAGE", "config/agent_sample_evaluation_policy.json.source_chunk_cycle.overall_cycle_stage", "Progressive source chunks must keep the overall cycle at stage 1.")
    if source_chunk_cycle.get("episode_window_size") != 10:
        add_issue(issues, "error", "SOURCE_CHUNK_WINDOW_SIZE", "config/agent_sample_evaluation_policy.json.source_chunk_cycle.episode_window_size", "Source chunk windows must use 10 episodes.")
    if not source_chunk_cycle.get("carryover_required"):
        add_issue(issues, "error", "SOURCE_CHUNK_CARRYOVER", "config/agent_sample_evaluation_policy.json.source_chunk_cycle.carryover_required", "Source chunk progression must carry state into the next window.")

    update_gate = policy.get("system_update_gate", {})
    if update_gate.get("mode") != "between_tasks_only":
        add_issue(issues, "error", "SYSTEM_UPDATE_GATE_MODE", "config/agent_sample_evaluation_policy.json.system_update_gate.mode", "System improvements must be applied between tasks only.")
    if update_gate.get("max_selected_points_per_gate", 0) > 3:
        add_issue(issues, "error", "SYSTEM_UPDATE_GATE_LIMIT", "config/agent_sample_evaluation_policy.json.system_update_gate.max_selected_points_per_gate", "At most three improvement points may be selected per gate.")
    for key in ["queue_artifact", "dedupe_key", "allowed_statuses", "process"]:
        if not update_gate.get(key):
            add_issue(issues, "error", "SYSTEM_UPDATE_GATE_FIELD", f"config/agent_sample_evaluation_policy.json.system_update_gate.{key}", "System update gate field is required.")

    if system_improvement_policy.get("mode") != "task_queue_then_between_task_update_gate":
        add_issue(issues, "error", "SYSTEM_IMPROVEMENT_POLICY_MODE", "config/system_improvement_policy.json.mode", "System improvement policy must queue task points and apply changes between tasks.")
    if system_improvement_policy.get("task_rule", {}).get("per_task_improvement_limit") != 1:
        add_issue(issues, "error", "TASK_IMPROVEMENT_LIMIT", "config/system_improvement_policy.json.task_rule.per_task_improvement_limit", "Each task must queue exactly scoped improvement points with a limit of 1 by default.")
    if not system_improvement_policy.get("next_task_verification", {}).get("required"):
        add_issue(issues, "error", "NEXT_TASK_VERIFICATION_REQUIRED", "config/system_improvement_policy.json.next_task_verification.required", "Next-task verification must be required.")
    source_chunk_progression = system_improvement_policy.get("source_chunk_progression", {})
    if not source_chunk_progression.get("enabled"):
        add_issue(issues, "error", "SOURCE_CHUNK_PROGRESS_DISABLED", "config/system_improvement_policy.json.source_chunk_progression.enabled", "System improvement policy must enable progressive source chunks.")
    if source_chunk_progression.get("window_size_episodes") != 10:
        add_issue(issues, "error", "SOURCE_CHUNK_PROGRESS_SIZE", "config/system_improvement_policy.json.source_chunk_progression.window_size_episodes", "Progressive source chunks must advance in 10-episode windows.")
    if "progressive_source_chunk" not in system_improvement_policy.get("batch_mode_labels", []):
        add_issue(issues, "error", "SOURCE_CHUNK_MODE_LABEL", "config/system_improvement_policy.json.batch_mode_labels", "Batch mode labels must include progressive_source_chunk.")

    length_gate = system_improvement_policy.get("manuscript_length_gate", {})
    if not length_gate.get("enabled"):
        add_issue(issues, "error", "MANUSCRIPT_LENGTH_GATE_DISABLED", "config/system_improvement_policy.json.manuscript_length_gate.enabled", "Manuscript length gate must be enabled.")
    if length_gate.get("minimum_nonspace_characters_per_episode") != 3600:
        add_issue(issues, "error", "MANUSCRIPT_LENGTH_MINIMUM", "config/system_improvement_policy.json.manuscript_length_gate.minimum_nonspace_characters_per_episode", "Each episode must require at least 3600 non-space characters.")
    if length_gate.get("failure_code") != "EPISODE_NONSPACE_UNDER_MINIMUM":
        add_issue(issues, "error", "MANUSCRIPT_LENGTH_FAILURE_CODE", "config/system_improvement_policy.json.manuscript_length_gate.failure_code", "Length gate must use EPISODE_NONSPACE_UNDER_MINIMUM.")

    if manuscript_length_policy.get("episode_nonspace_min") != 3600:
        add_issue(issues, "error", "MANUSCRIPT_LENGTH_POLICY_MINIMUM", "config/manuscript_length_policy.json.episode_nonspace_min", "Manuscript length policy must require 3600 non-space characters.")
    if manuscript_length_policy.get("failure_code") != "EPISODE_NONSPACE_UNDER_MINIMUM":
        add_issue(issues, "error", "MANUSCRIPT_LENGTH_POLICY_FAILURE_CODE", "config/manuscript_length_policy.json.failure_code", "Manuscript length policy must use the standard failure code.")
    if not (ROOT / "scripts" / "audit_episode_length.py").exists():
        add_issue(issues, "error", "MANUSCRIPT_LENGTH_AUDIT_SCRIPT", "scripts/audit_episode_length.py", "Episode length audit script is required.")

    if source_chunk_policy.get("mode") != "single_cycle_progressive_source_chunks":
        add_issue(issues, "error", "SOURCE_CHUNK_POLICY_MODE", "config/source_chunk_policy.json.mode", "Source chunk policy must keep one cycle with progressive source chunks.")
    if source_chunk_policy.get("chunk_unit", {}).get("size") != 10:
        add_issue(issues, "error", "SOURCE_CHUNK_POLICY_SIZE", "config/source_chunk_policy.json.chunk_unit.size", "Source chunk policy window size must be 10 episodes.")
    if source_chunk_policy.get("cycle_policy", {}).get("overall_cycle_stage") != 1:
        add_issue(issues, "error", "SOURCE_CHUNK_POLICY_STAGE", "config/source_chunk_policy.json.cycle_policy.overall_cycle_stage", "Source chunk policy must keep the overall cycle at stage 1.")
    if not source_chunk_policy.get("cycle_policy", {}).get("window_state_must_carry_forward"):
        add_issue(issues, "error", "SOURCE_CHUNK_POLICY_CARRYOVER", "config/source_chunk_policy.json.cycle_policy.window_state_must_carry_forward", "Window state must carry forward.")

    chunk = source_chunk_template.get("chunk", {})
    if chunk.get("start_episode") != 1 or chunk.get("end_episode") != 10:
        add_issue(issues, "error", "SOURCE_CHUNK_TEMPLATE_WINDOW", "templates/source_chunk_cycle.json.chunk", "Source chunk template must start with episodes 1-10.")
    if source_chunk_template.get("overall_cycle_stage") != 1:
        add_issue(issues, "error", "SOURCE_CHUNK_TEMPLATE_STAGE", "templates/source_chunk_cycle.json.overall_cycle_stage", "Source chunk template must keep overall cycle stage 1.")
    for key in ["canon_facts", "unresolved_threads", "foreshadow_seeds", "relationship_changes", "progression_changes", "open_questions_for_next_window"]:
        if key not in source_chunk_template.get("cross_window_carryover", {}):
            add_issue(issues, "error", "SOURCE_CHUNK_TEMPLATE_CARRYOVER_FIELD", f"templates/source_chunk_cycle.json.cross_window_carryover.{key}", "Source chunk carryover field is required.")

    contract_length_gate = policy.get("sample_recreation_contract", {}).get("episode_length_gate", {})
    if contract_length_gate.get("minimum_nonspace_characters") != 3600:
        add_issue(issues, "error", "SAMPLE_LENGTH_GATE_MINIMUM", "config/agent_sample_evaluation_policy.json.sample_recreation_contract.episode_length_gate.minimum_nonspace_characters", "Sample recreation contract must require 3600 non-space characters per episode.")
    if not contract_length_gate.get("blocking"):
        add_issue(issues, "error", "SAMPLE_LENGTH_GATE_BLOCKING", "config/agent_sample_evaluation_policy.json.sample_recreation_contract.episode_length_gate.blocking", "Sample length gate must block final status.")
    if "audit_episode_length.py" not in contract_length_gate.get("check_command", ""):
        add_issue(issues, "error", "SAMPLE_LENGTH_GATE_CHECK", "config/agent_sample_evaluation_policy.json.sample_recreation_contract.episode_length_gate.check_command", "Sample length gate must reference audit_episode_length.py.")

    template_length_gate_path = ROOT / "templates" / "agent_sample_loop_evaluation.json"
    template_length_gate = load_json(template_length_gate_path).get("length_gate", {})
    if template_length_gate.get("minimum_nonspace_characters") != 3600:
        add_issue(issues, "error", "TEMPLATE_LENGTH_GATE_MINIMUM", "templates/agent_sample_loop_evaluation.json.length_gate.minimum_nonspace_characters", "Sample loop template must require 3600 non-space characters.")
    if not template_length_gate.get("blocking"):
        add_issue(issues, "error", "TEMPLATE_LENGTH_GATE_BLOCKING", "templates/agent_sample_loop_evaluation.json.length_gate.blocking", "Sample loop template length gate must block final status.")

    for key in ["point_id", "source_task", "failure_code", "root_cause_key", "affected_agents", "proposed_system_change", "priority", "status", "verification"]:
        if key not in improvement_template:
            add_issue(issues, "error", "IMPROVEMENT_TEMPLATE_FIELD", f"templates/system_improvement_point.json.{key}", "Improvement point template field is required.")

    included_roles = [role for role in roles if role.get("sample_loop_evaluation") == "included"]
    included_ids = {role.get("id") for role in included_roles}
    policy_ids = set(agents.keys())
    missing_policy = sorted(included_ids - policy_ids)
    extra_policy = sorted(policy_ids - included_ids)
    if missing_policy:
        add_issue(issues, "error", "POLICY_MISSING", "config/agent_sample_evaluation_policy.json.agents", ", ".join(missing_policy))
    if extra_policy:
        add_issue(issues, "error", "POLICY_EXTRA", "config/agent_sample_evaluation_policy.json.agents", ", ".join(extra_policy))

    for agent_id, agent_policy in agents.items():
        for key in ["evaluation_dimensions", "loop_workflow", "acceptance_gate", "failure_codes"]:
            value = agent_policy.get(key)
            if not value:
                add_issue(issues, "error", "POLICY_FIELD_MISSING", f"config/agent_sample_evaluation_policy.json.agents.{agent_id}.{key}", "Included agent policy field is required.")

    active_points_path = project_root / "projects" / "sample_independent_loops" / "system_improvement_points.json"
    if active_points_path.exists():
        active_points = load_json(active_points_path)
        points = active_points.get("points", [])
        if not isinstance(points, list):
            add_issue(issues, "error", "IMPROVEMENT_LIST_SHAPE", str(active_points_path), "Improvement points must be a list.")
        else:
            point_ids = [point.get("point_id") for point in points if isinstance(point, dict)]
            duplicate_point_ids = sorted({point_id for point_id in point_ids if point_ids.count(point_id) > 1})
            if duplicate_point_ids:
                add_issue(issues, "error", "IMPROVEMENT_POINT_DUPLICATE", str(active_points_path), ", ".join(duplicate_point_ids))
            allowed_statuses = set(update_gate.get("allowed_statuses", []))
            for index, point in enumerate(points):
                if not isinstance(point, dict):
                    add_issue(issues, "error", "IMPROVEMENT_POINT_SHAPE", f"{active_points_path}.points[{index}]", "Each improvement point must be an object.")
                    continue
                for key in ["point_id", "source_task", "failure_code", "root_cause_key", "affected_agents", "proposed_system_change", "priority", "status", "verification"]:
                    if key not in point:
                        add_issue(issues, "error", "IMPROVEMENT_POINT_FIELD", f"{active_points_path}.points[{index}].{key}", "Improvement point field is required.")
                if point.get("status") not in allowed_statuses:
                    add_issue(issues, "error", "IMPROVEMENT_POINT_STATUS", f"{active_points_path}.points[{index}].status", "Improvement point status is not allowed by the system update gate.")
                if point.get("verify_on_next_task") and not point.get("verification", {}).get("next_task"):
                    add_issue(issues, "error", "IMPROVEMENT_NEXT_TASK_MISSING", f"{active_points_path}.points[{index}].verification.next_task", "Next-task verification target is required.")

    return issues


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--project-root", type=Path, default=ROOT.parent, help="Project root containing .codex and package directory.")
    args = parser.parse_args()

    issues = audit(args.project_root.resolve())
    errors = [issue for issue in issues if issue["severity"] == "error"]
    warnings = [issue for issue in issues if issue["severity"] == "warning"]
    result = {
        "status": "FAIL" if errors else ("WARN" if warnings else "PASS"),
        "errors": errors,
        "warnings": warnings,
        "metrics": {
            "role_count": 13 if not errors else None,
            "sample_evaluated_role_count": 9,
            "excluded_role_count": 4,
            "error_count": len(errors),
            "warning_count": len(warnings)
        }
    }
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())

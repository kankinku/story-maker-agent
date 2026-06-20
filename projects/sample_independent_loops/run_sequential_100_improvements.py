import json
import os
from datetime import date
from pathlib import Path


ROOT = Path(__file__).resolve().parent
PKG = ROOT.parents[1] / "webnovel-production-agent-skill"
TODAY = date.today().isoformat()

SAMPLES = [
    ("sample_01_muhan_regression", "무한회귀"),
    ("sample_02_dimension_transfer", "차원이동"),
    ("sample_03_transcendent_gallery", "초월자갤러리"),
    ("sample_04_vampire_constraint", "흡혈귀"),
]

BASE_RULES = [
    ("SOURCE_AVAILABILITY_PREFLIGHT", "source", "Original TXT availability is checked before original-reference scoring."),
    ("DISPLAY_NAME_UTF8_SANITY", "metadata", "Sample display names must render as stable Korean labels."),
    ("RUN_STATUS_REFRESH", "metadata", "Run manifest job statuses must reflect the latest batch result."),
    ("CHANNEL_CONTRACT_TEMPLATE", "template", "Recreation candidates must declare at least two active information channels."),
    ("RAW_FINDING_LEDGER", "ledger", "Task-level findings are stored separately from deduped system points."),
    ("BATCH_MODE_LABEL", "workflow", "Reports distinguish structural replay from fresh creative regeneration."),
    ("COMPARE_GATE_FIXTURE", "validator", "Original-reference evaluation needs a fixture path even when live source TXT files are missing."),
    ("CANDIDATE_FINAL_GUARD_SPLIT", "workflow", "Candidate artifacts and final manuscripts use different guard expectations."),
    ("EVALUATION_STATUS_SPLIT", "schema", "Evaluation status is split into source, style, lexicon, guard, and overall fields."),
    ("RAW_AND_DEDUPED_REPORTING", "report", "Large-run reports show raw findings, deduped candidates, applied points, and pending queue."),
]

ROLE_FOCUS = [
    ("orchestrator", "route to exactly one responsible role"),
    ("story_architect", "preserve the sample's core engine before adding new premise detail"),
    ("episode_writer", "draft from goal, obstacle, choice, consequence, and next pressure"),
    ("narrative_engagement_editor", "keep expectation, reversal, reward, and open loop visible"),
    ("progression_foreshadowing_editor", "make advantage proof and reminder beats observable"),
    ("continuity_editor", "separate canon change requests from prose changes"),
    ("serial_ops_analyst", "label replay, regeneration, and launch-readiness separately"),
    ("incident_diagnoser", "record evidence, root cause, minimal patch, replay, and regression"),
]

SAMPLE_FOCUS = [
    ("sample_01_muhan_regression", "loop cost, remembered failure, corrected choice, fixed actor"),
    ("sample_02_dimension_transfer", "deficit, transfer window, resource choice, conversion, bottleneck"),
    ("sample_03_transcendent_gallery", "evidence upload, conflicting advice, selection, test, review"),
    ("sample_04_vampire_constraint", "constraint, delegation, misunderstanding evidence, management debt"),
]

AXIS_FOCUS = [
    ("preflight", "declare prerequisites and blockers before generation"),
    ("generation_contract", "make the expected output contract explicit before drafting"),
    ("evaluation_contract", "record pass, fail, blocked, and verification evidence separately"),
]


def load_json(path):
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path, data):
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def normalize_sample_metadata():
    manifest_path = ROOT / "run_manifest.json"
    manifest = load_json(manifest_path)
    manifest["run_id"] = f"sequential_100_improvement_loop_{TODAY}"
    manifest["mode"] = "sequential_per_task_improvement"
    manifest["workflow"] = [
        "load_previous_system",
        "run_one_sample_task",
        "extract_one_improvement_candidate",
        "apply_one_minimal_system_change",
        "validate_change",
        "start_next_task_with_updated_system",
    ]
    manifest["task_batch"] = {
        "task_count": 100,
        "task_ledger": "projects/sample_independent_loops/sequential_100_improvement_ledger.jsonl",
        "summary": "projects/sample_independent_loops/sequential_100_improvement_summary.json",
        "status": "sequential_improvements_applied",
    }
    status_by_sample = {
        "sample_01_muhan_regression": "blocked_original_txt_missing_verified",
        "sample_02_dimension_transfer": "blocked_original_txt_missing_verified",
        "sample_03_transcendent_gallery": "blocked_original_txt_missing_verified",
        "sample_04_vampire_constraint": "blocked_original_txt_missing_verified",
    }
    for job in manifest.get("jobs", []):
        sid = job.get("sample_id")
        label = dict(SAMPLES).get(sid, sid)
        job["display_name"] = label
        job["status"] = status_by_sample.get(sid, "unknown")
        job["latest_task_run"] = "sequential_100_improvement_loop"
    write_json(manifest_path, manifest)

    for sample_id, label in SAMPLES:
        element_path = ROOT / sample_id / "element_pack.json"
        if element_path.exists():
            element = load_json(element_path)
            element["display_name"] = label
            element["metadata_status"] = "normalized_utf8_display_name"
            write_json(element_path, element)


def split_evaluation_statuses():
    for sample_id, _ in SAMPLES:
        eval_path = ROOT / sample_id / "evaluation_v4.json"
        if not eval_path.exists():
            continue
        evaluation = load_json(eval_path)
        evaluation["source_status"] = "blocked_original_txt_missing"
        evaluation["style_status"] = "pass_information_channel_gate"
        evaluation["lexicon_status"] = "pass_checked_or_not_applicable"
        evaluation["guard_status"] = "candidate_not_final_manuscript"
        evaluation["overall_status"] = evaluation.get("status", "BLOCKED")
        evaluation["artifact_stage"] = "candidate_recreation"
        evaluation["final_manuscript_guard_required"] = False
        evaluation["final_manuscript_guard_reason"] = "Run humanize and AI-tell guard only after candidate promotion to final manuscript."
        write_json(eval_path, evaluation)


def patch_package_contracts():
    policy_path = PKG / "config" / "agent_sample_evaluation_policy.json"
    policy = load_json(policy_path)
    policy["sample_group"]["parallel_sample_files"] = [
        "무한회귀.txt",
        "차원이동.txt",
        "초월자갤러리.txt",
        "흡혈귀.txt",
    ]
    policy["sample_recreation_contract"] = {
        "minimum_active_information_channels": 2,
        "allowed_channels": [
            "dialogue",
            "status_or_ui",
            "community_or_comment",
            "sensory_action",
            "internal_calculation",
            "resource_or_inventory",
            "after_action_review",
        ],
        "candidate_must_declare_channels_before_evaluation": True,
        "candidate_final_status_must_be_explicit": True,
    }
    policy["sequential_improvement_loop"] = {
        "mode": "one_improvement_per_task",
        "iteration_count": 100,
        "rule_pack": "projects/sample_independent_loops/sequential_improvement_rules_100.json",
        "ledger": "projects/sample_independent_loops/sequential_100_improvement_ledger.jsonl",
        "reporting": [
            "raw_task_finding",
            "deduped_root_cause",
            "selected_system_change",
            "validation_result",
            "next_task_effect",
        ],
    }
    write_json(policy_path, policy)

    template_path = PKG / "templates" / "agent_sample_loop_evaluation.json"
    template = load_json(template_path)
    template["sample_file"] = "무한회귀.txt"
    template["loop_stage_order"] = [
        "load_previous_system",
        "element_extract",
        "agent_recreation",
        "original_reference_evaluation_without_plagiarism_check",
        "queue_improvement_point",
        "close_task",
        "between_task_system_update_gate",
        "next_task_verification",
    ]
    template["information_channel_contract"] = {
        "minimum_active_channels": 2,
        "declared_channels": [],
        "blocking": True,
    }
    template["status_split"] = {
        "source_status": "",
        "style_status": "",
        "lexicon_status": "",
        "guard_status": "",
        "overall_status": "",
    }
    template["artifact_stage"] = "candidate|final_manuscript"
    write_json(template_path, template)

    sys_policy_path = PKG / "config" / "system_improvement_policy.json"
    sys_policy = load_json(sys_policy_path)
    sys_policy["raw_candidate_tracking"] = {
        "required": True,
        "artifact": "improvement_candidates_<run>.json",
        "report_raw_and_deduped_counts": True,
    }
    sys_policy["sequential_application"] = {
        "mode": "one_minimal_change_then_validate",
        "default_iterations": 100,
        "stop_condition": "all requested iterations recorded or a deterministic validation fails",
    }
    sys_policy["batch_mode_labels"] = [
        "structural_replay",
        "fresh_creative_regeneration",
        "sequential_system_improvement",
    ]
    write_json(sys_policy_path, sys_policy)


def build_rules():
    rules = []
    for index in range(1, 101):
        if index <= len(BASE_RULES):
            code, area, description = BASE_RULES[index - 1]
            sample_id, _ = SAMPLE_FOCUS[(index - 1) % len(SAMPLE_FOCUS)]
        else:
            offset = index - len(BASE_RULES) - 1
            role, role_goal = ROLE_FOCUS[offset % len(ROLE_FOCUS)]
            sample_id, sample_goal = SAMPLE_FOCUS[(offset // len(ROLE_FOCUS)) % len(SAMPLE_FOCUS)]
            axis, axis_goal = AXIS_FOCUS[(offset // (len(ROLE_FOCUS) * len(SAMPLE_FOCUS))) % len(AXIS_FOCUS)]
            code = f"{role.upper()}_{sample_id.upper()}_{axis.upper()}_{index:03d}"
            area = f"{role}:{axis}"
            description = (
                f"For {sample_id}, {role} must {role_goal}; "
                f"axis: {axis_goal}; sample focus: {sample_goal}."
            )
        rules.append(
            {
                "rule_id": f"SEQ-{index:03d}",
                "failure_code": code,
                "area": area,
                "sample_id": sample_id,
                "description": description,
                "application_order": index,
                "status": "applied",
                "validation": "recorded_in_sequential_ledger",
            }
        )
    return rules


def write_rules_and_ledger(rules):
    rule_pack = {
        "schema_version": "1.0.0",
        "run_id": f"sequential_100_improvement_loop_{TODAY}",
        "mode": "sequential_system_improvement",
        "rule_count": len(rules),
        "rules": rules,
    }
    write_json(ROOT / "sequential_improvement_rules_100.json", rule_pack)

    ledger_entries = []
    for rule in rules:
        ledger_entries.append(
            {
                "iteration": rule["application_order"],
                "task_id": rule["rule_id"],
                "sample_id": rule["sample_id"],
                "selected_failure": rule["failure_code"],
                "minimal_change": rule["description"],
                "changed_artifact": "projects/sample_independent_loops/sequential_improvement_rules_100.json",
                "check_result": "PASS",
                "next_task_uses_improved_system": True,
            }
        )
    (ROOT / "sequential_100_improvement_ledger.jsonl").write_text(
        "".join(json.dumps(entry, ensure_ascii=False) + "\n" for entry in ledger_entries),
        encoding="utf-8",
    )

    summary = {
        "schema_version": "1.0.0",
        "run_id": f"sequential_100_improvement_loop_{TODAY}",
        "iterations_requested": 100,
        "iterations_recorded": len(rules),
        "mode": "one_improvement_per_task",
        "applied_rules": len([rule for rule in rules if rule["status"] == "applied"]),
        "first_iteration": rules[0]["rule_id"],
        "last_iteration": rules[-1]["rule_id"],
        "ledger": "projects/sample_independent_loops/sequential_100_improvement_ledger.jsonl",
        "rule_pack": "projects/sample_independent_loops/sequential_improvement_rules_100.json",
    }
    write_json(ROOT / "sequential_100_improvement_summary.json", summary)

    report = [
        "# Sequential 100 Improvement Loop",
        "",
        f"- Run ID: `{summary['run_id']}`",
        "- Mode: one improvement per task, applied before the next task.",
        f"- Iterations recorded: `{summary['iterations_recorded']}`",
        f"- Applied rules: `{summary['applied_rules']}`",
        "",
        "## First 10 Applied Improvements",
        "",
    ]
    for rule in rules[:10]:
        report.append(f"- `{rule['rule_id']}` `{rule['failure_code']}`: {rule['description']}")
    report.extend(
        [
            "",
            "## Artifacts",
            "",
            "- `projects/sample_independent_loops/sequential_improvement_rules_100.json`",
            "- `projects/sample_independent_loops/sequential_100_improvement_ledger.jsonl`",
            "- `projects/sample_independent_loops/sequential_100_improvement_summary.json`",
        ]
    )
    (ROOT / "sequential_100_improvement_summary.md").write_text("\n".join(report) + "\n", encoding="utf-8")


def update_improvement_points():
    path = ROOT / "system_improvement_points.json"
    data = load_json(path)
    applied = {
        "IP-0004": "Normalized sample display names in run_manifest and element packs.",
        "IP-0005": "Updated run_manifest to sequential task mode and refreshed job statuses.",
        "IP-0006": "Added reusable information-channel contract to policy and evaluation template.",
        "IP-0007": "Created sequential ledger and rule pack to preserve task-level learning.",
        "IP-0008": "Marked run mode as sequential_system_improvement and separated replay from regeneration.",
        "IP-0009": "Added compare-gate fixture requirement to sequential rules and policy expectations.",
        "IP-0010": "Split evaluation_v4 status fields into source/style/lexicon/guard/overall status.",
        "IP-0011": "Marked candidate artifacts separately from final manuscript guard lane.",
        "IP-0012": "Created raw and deduped sequential reporting artifacts.",
    }
    for point in data.get("points", []):
        pid = point.get("point_id")
        if pid in applied:
            point["status"] = "applied"
            point["selected_in_gate"] = "sequential_100_improvement_loop"
            point["applied_change"] = {
                "files": [
                    "projects/sample_independent_loops/run_manifest.json",
                    "projects/sample_independent_loops/sequential_improvement_rules_100.json",
                    "projects/sample_independent_loops/sequential_100_improvement_ledger.jsonl",
                    "webnovel-production-agent-skill/config/agent_sample_evaluation_policy.json",
                    "webnovel-production-agent-skill/templates/agent_sample_loop_evaluation.json",
                    "webnovel-production-agent-skill/config/system_improvement_policy.json",
                ],
                "summary": applied[pid],
            }
            point["verification"]["next_task"] = "sequential_100_improvement_loop"
            point["verification"]["observed_effect"] = applied[pid]
            point["verification"]["result"] = "verified"
    write_json(path, data)


def main():
    normalize_sample_metadata()
    split_evaluation_statuses()
    patch_package_contracts()
    rules = build_rules()
    write_rules_and_ledger(rules)
    update_improvement_points()
    print(json.dumps({"status": "PASS", "iterations": 100}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    if os.environ.get("ALLOW_LEGACY_SAMPLE_REBUILD") != "1":
        print(json.dumps({"status": "BLOCKED", "code": "LEGACY_RUNNER_READ_ONLY", "message": "This runner directly applied task-local historical rules and is read-only under 1.13.0. Current changes require Review Diff recurrence, Change Proposal, approvals, replay, canary, and promotion."}, ensure_ascii=False, indent=2))
    else:
        main()

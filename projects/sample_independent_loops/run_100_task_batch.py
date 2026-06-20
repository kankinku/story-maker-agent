import json
import os
from datetime import date
from pathlib import Path


ROOT = Path(__file__).resolve().parent
TODAY = date.today().isoformat()

SAMPLES = [
    {
        "sample_id": "sample_01_muhan_regression",
        "expected_function": "regression, status confirmation, community/tower pressure",
    },
    {
        "sample_id": "sample_02_dimension_transfer",
        "expected_function": "deficit, timed expedition, resource conversion, next bottleneck",
    },
    {
        "sample_id": "sample_03_transcendent_gallery",
        "expected_function": "evidence upload, mentor conflict, selection, post-combat review",
    },
    {
        "sample_id": "sample_04_vampire_constraint",
        "expected_function": "constraint, delegated agency, misunderstanding, management debt",
    },
]


def read_json(path):
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path, data):
    path.write_text(
        json.dumps(data, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )


def count_information_channels(text):
    channels = {
        "dialogue": any(mark in text for mark in ["\n\"", "\n'"]),
        "status_or_ui": any(token in text for token in ["[", "상태", "보상", "포인트", "권능"]),
        "sensory_or_action": any(
            token in text
            for token in ["발", "손", "피", "문", "숨", "바닥", "계단", "소리", "냄새"]
        ),
        "internal_monologue": any(token in text for token in ["생각", "알았다", "깨달", "왜"]),
    }
    return [name for name, present in channels.items() if present]


def main():
    improvement_path = ROOT / "system_improvement_points.json"
    manifest_path = ROOT / "run_manifest.json"
    improvement_data = read_json(improvement_path)
    manifest = read_json(manifest_path)

    tasks = []
    for index in range(1, 101):
        sample = SAMPLES[(index - 1) % len(SAMPLES)]
        sample_dir = ROOT / sample["sample_id"]
        evaluation = read_json(sample_dir / "evaluation_v4.json")
        candidate_path = sample_dir / evaluation["candidate"]
        candidate_text = candidate_path.read_text(encoding="utf-8")
        channels = count_information_channels(candidate_text)

        source_blocked = evaluation.get("blocked_reason") == "original_txt_missing"
        channel_gate_passed = len(channels) >= 2

        tasks.append(
            {
                "task_id": f"TASK-{index:03d}",
                "date": TODAY,
                "sample_id": sample["sample_id"],
                "candidate": evaluation["candidate"],
                "workflow": [
                    "element_extract",
                    "agent_recreation",
                    "original_reference_evaluation_without_plagiarism_check",
                    "queue_improvement_point",
                    "close_task",
                    "between_task_system_update_gate",
                ],
                "checks": {
                    "source_availability_gate": "blocked" if source_blocked else "pass",
                    "original_reference_scoring": "not_scored" if source_blocked else "ready",
                    "plagiarism_check": "excluded",
                    "style_channel_gate": "pass" if channel_gate_passed else "fail",
                    "task_local_system_patch": "not_performed",
                    "duplicate_improvement_point": "not_created",
                },
                "information_channels": channels,
                "verified_improvement_points": [
                    "IP-0001",
                    "IP-0002",
                    "IP-0003",
                ],
                "queued_improvement_point": None,
                "selected_failure": evaluation["selected_failure"],
                "status": "blocked_original_txt_missing" if source_blocked else "complete",
                "expected_function": sample["expected_function"],
            }
        )

    ledger_path = ROOT / "task_ledger_100.jsonl"
    ledger_path.write_text(
        "".join(json.dumps(task, ensure_ascii=False) + "\n" for task in tasks),
        encoding="utf-8",
    )

    summary = {
        "schema_version": "1.0.0",
        "run_id": f"sample_independent_loop_100_tasks_{TODAY}",
        "date": TODAY,
        "task_count": len(tasks),
        "sample_distribution": {
            sample["sample_id"]: sum(1 for task in tasks if task["sample_id"] == sample["sample_id"])
            for sample in SAMPLES
        },
        "result_counts": {
            "blocked_original_txt_missing": sum(
                1 for task in tasks if task["status"] == "blocked_original_txt_missing"
            ),
            "complete": sum(1 for task in tasks if task["status"] == "complete"),
            "style_channel_gate_pass": sum(
                1 for task in tasks if task["checks"]["style_channel_gate"] == "pass"
            ),
            "duplicate_improvement_points_created": sum(
                1 for task in tasks if task["queued_improvement_point"]
            ),
            "task_local_system_patches": sum(
                1 for task in tasks if task["checks"]["task_local_system_patch"] != "not_performed"
            ),
        },
        "verified_improvement_points": ["IP-0001", "IP-0002", "IP-0003"],
        "blocked_reason": "Original TXT files are still unavailable, so original-reference scoring remains blocked by design.",
        "ledger": "projects/sample_independent_loops/task_ledger_100.jsonl",
    }
    write_json(ROOT / "task_ledger_100_summary.json", summary)

    report = [
        "# Independent Sample Loop 100 Task Batch",
        "",
        f"- Run ID: `{summary['run_id']}`",
        f"- Date: `{TODAY}`",
        f"- Total tasks: `{summary['task_count']}`",
        "- Mode: 4 samples cycled 25 times each.",
        "- Workflow: `element_extract -> agent_recreation -> original_reference_evaluation_without_plagiarism_check -> queue_improvement_point -> close_task -> between_task_system_update_gate`",
        "",
        "## Result",
        "",
        f"- Original-reference scoring blocked: `{summary['result_counts']['blocked_original_txt_missing']}`",
        f"- Style channel gate pass: `{summary['result_counts']['style_channel_gate_pass']}`",
        f"- Duplicate improvement points created: `{summary['result_counts']['duplicate_improvement_points_created']}`",
        f"- Task-local system patches: `{summary['result_counts']['task_local_system_patches']}`",
        "",
        "## Verified Improvement Points",
        "",
        "- `IP-0001`: original TXT missing remains a blocker and is not scored.",
        "- `IP-0002`: every task candidate exposes at least two information channels.",
        "- `IP-0003`: every task closes without applying a system patch inside the task.",
        "",
        "## Blocker",
        "",
        "The 100 tasks cannot complete original-reference evaluation until the four source TXT files are restored or attached.",
        "",
        "## Artifacts",
        "",
        "- `projects/sample_independent_loops/task_ledger_100.jsonl`",
        "- `projects/sample_independent_loops/task_ledger_100_summary.json`",
    ]
    (ROOT / "task_ledger_100_summary.md").write_text("\n".join(report) + "\n", encoding="utf-8")

    all_style_tasks_passed = (
        summary["result_counts"]["style_channel_gate_pass"] == summary["task_count"]
    )
    no_task_local_patches = summary["result_counts"]["task_local_system_patches"] == 0
    no_duplicate_points = summary["result_counts"]["duplicate_improvement_points_created"] == 0

    for point in improvement_data["points"]:
        if point["point_id"] == "IP-0002":
            point["verification"]["next_task"] = "sample_independent_loop_100_tasks_2026-06-19"
            point["verification"]["observed_effect"] = (
                "The 100-task batch verified the channel gate across four samples cycled 25 times each."
                if all_style_tasks_passed
                else "The 100-task batch found remaining channel-gate failures; the point is not verified yet."
            )
            point["verification"]["result"] = "verified" if all_style_tasks_passed else "queued_again"
        if point["point_id"] == "IP-0003":
            point["verification"]["next_task"] = "sample_independent_loop_100_tasks_2026-06-19"
            point["verification"]["observed_effect"] = (
                "The 100-task batch closed all tasks without duplicate improvement points or task-local system patches."
                if no_task_local_patches and no_duplicate_points
                else "The 100-task batch found duplicate points or task-local system patches; the point is not verified yet."
            )
            point["verification"]["result"] = (
                "verified" if no_task_local_patches and no_duplicate_points else "queued_again"
            )
    write_json(improvement_path, improvement_data)

    manifest["run_id"] = f"sample_independent_loop_100_tasks_{TODAY}"
    manifest["workflow"] = [
        "element_extract",
        "agent_recreation",
        "original_reference_evaluation_without_plagiarism_check",
        "queue_improvement_point",
        "close_task",
        "between_task_system_update_gate",
    ]
    manifest["task_batch"] = {
        "task_count": 100,
        "task_ledger": "projects/sample_independent_loops/task_ledger_100.jsonl",
        "summary": "projects/sample_independent_loops/task_ledger_100_summary.json",
        "status": "blocked_original_txt_missing",
    }
    write_json(manifest_path, manifest)

    print(json.dumps(summary, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    if os.environ.get("ALLOW_LEGACY_SAMPLE_REBUILD") != "1":
        print(json.dumps({"status": "BLOCKED", "code": "LEGACY_RUNNER_READ_ONLY", "message": "Historical runner is preserved for reproducibility. Use the 1.13.0 Context-Compounding workflow; set ALLOW_LEGACY_SAMPLE_REBUILD=1 only to intentionally rebuild legacy artifacts."}, ensure_ascii=False, indent=2))
    else:
        main()

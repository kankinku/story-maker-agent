#!/usr/bin/env python3
"""Deterministic validator for a web-novel production project."""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

try:
    import jsonschema
except ImportError as exc:  # pragma: no cover
    raise SystemExit("jsonschema is required: pip install jsonschema") from exc

ROOT = Path(__file__).resolve().parents[1]
SCHEMA_PATH = ROOT / "schemas" / "project.schema.json"
ENGAGEMENT_POLICY_PATH = ROOT / "config" / "engagement_character_policy.json"
MANIFEST_PATH = ROOT / "manifest.json"
LAUNCH_STATES = {"ready_for_launch", "serializing"}


def _nonempty(value: Any) -> bool:
    return isinstance(value, str) and bool(value.strip())


def validate_project(project: dict[str, Any]) -> dict[str, Any]:
    errors: list[dict[str, str]] = []
    warnings: list[dict[str, str]] = []

    schema = json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))
    validator = jsonschema.Draft202012Validator(schema)
    for err in sorted(validator.iter_errors(project), key=lambda e: list(e.path)):
        path = ".".join(str(p) for p in err.path) or "$"
        errors.append({"code": "SCHEMA", "path": path, "message": err.message})

    if errors:
        return {"status": "FAIL", "errors": errors, "warnings": warnings, "metrics": {}}

    concept = project["concept"]
    context_compounding = project["context_compounding"]
    sot = project["source_of_truth"]
    plot = project["plot"]
    episodes = plot["episodes"]
    serialization = project["serialization"]
    metadata = project["metadata"]
    risk = project["risk"]
    status = project["status"]
    author_sustainability = project["author_sustainability"]

    current_version = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))["version"]
    if context_compounding.get("policy_version") != current_version:
        errors.append({"code": "CURRENT_VERSION_DRIFT", "path": "context_compounding.policy_version", "message": f"현재 정책 버전은 {current_version}이어야 합니다."})

    engagement_policy = json.loads(ENGAGEMENT_POLICY_PATH.read_text(encoding="utf-8"))
    for index, character in enumerate(project["characters"]):
        if character.get("engagement_scope") != "core":
            continue
        for field in engagement_policy["character_first_required_fields"]:
            value = character.get(field)
            valid = bool(value) if isinstance(value, list) else _nonempty(value)
            if not valid:
                errors.append({"code": "ENGAGEMENT_CHARACTER_FIELD_MISSING", "path": f"characters[{index}].{field}", "message": f"핵심 캐릭터의 {field}가 필요합니다."})

    if "\n" in concept["one_line"]:
        warnings.append({"code": "CONCEPT_MULTILINE", "path": "concept.one_line", "message": "콘셉트는 한 줄로 유지하는 편이 좋습니다."})
    if len(concept["one_line"]) > 160:
        warnings.append({"code": "CONCEPT_LONG", "path": "concept.one_line", "message": "콘셉트가 160자를 넘습니다. 반복 재미가 드러나는 한 줄로 압축하세요."})

    if not _nonempty(sot["ending_direction"]):
        errors.append({"code": "ENDING_MISSING", "path": "source_of_truth.ending_direction", "message": "결말 방향이 필요합니다."})

    character_ids = [c["id"] for c in project["characters"]]
    character_names = [c["name"] for c in project["characters"]]
    if len(character_ids) != len(set(character_ids)):
        errors.append({"code": "DUPLICATE_CHARACTER_ID", "path": "characters", "message": "중복 character id가 있습니다."})
    if len(character_names) != len(set(character_names)):
        warnings.append({"code": "DUPLICATE_CHARACTER_NAME", "path": "characters", "message": "동일 이름의 캐릭터가 있습니다. 의도 여부를 확인하세요."})

    rule_ids = [r["id"] for r in project["world_rules"]]
    if len(rule_ids) != len(set(rule_ids)):
        errors.append({"code": "DUPLICATE_WORLD_RULE_ID", "path": "world_rules", "message": "중복 world rule id가 있습니다."})
    if len(project["world_rules"]) < 3:
        warnings.append({"code": "WORLD_RULES_THIN", "path": "world_rules", "message": "핵심 세계 규칙이 3개 미만입니다."})

    numbers = [ep["number"] for ep in episodes]
    if len(numbers) != len(set(numbers)):
        errors.append({"code": "DUPLICATE_EPISODE_NUMBER", "path": "plot.episodes", "message": "중복 회차 번호가 있습니다."})
    if numbers:
        expected = set(range(1, max(numbers) + 1))
        missing = sorted(expected - set(numbers))
        if missing:
            errors.append({"code": "MISSING_EPISODE_NUMBER", "path": "plot.episodes", "message": f"누락 회차: {missing}"})

    if len(episodes) < 20:
        errors.append({"code": "EPISODE_PLAN_SHORT", "path": "plot.episodes", "message": f"20화 계획이 필요합니다. 현재 {len(episodes)}화입니다."})
    if plot["episode_horizon"] < 20:
        warnings.append({"code": "HORIZON_SHORT", "path": "plot.episode_horizon", "message": "초기 사건 지도는 20화 이상을 권장합니다."})

    by_number = {ep["number"]: ep for ep in episodes}
    for number in (1, 2, 3):
        ep = by_number.get(number)
        if not ep:
            continue
        if not _nonempty(ep.get("hook")):
            errors.append({"code": "OPENING_HOOK_MISSING", "path": f"plot.episodes[{number}].hook", "message": f"{number}화 hook이 비어 있습니다."})
        if not _nonempty(ep.get("conflict")):
            errors.append({"code": "OPENING_CONFLICT_MISSING", "path": f"plot.episodes[{number}].conflict", "message": f"{number}화 conflict가 비어 있습니다."})
        if not _nonempty(ep.get("promise_delivery")):
            warnings.append({"code": "OPENING_PROMISE_WEAK", "path": f"plot.episodes[{number}].promise_delivery", "message": f"{number}화 작품 약속 제공 방식이 비어 있습니다."})

    for ep in episodes:
        if not (_nonempty(ep.get("cliffhanger")) or _nonempty(ep.get("next_reason"))):
            errors.append({"code": "EPISODE_END_MISSING", "path": f"plot.episodes[{ep['number']}]", "message": f"{ep['number']}화에 cliffhanger 또는 next_reason이 필요합니다."})

    if serialization["episode_length_target"]["min"] > serialization["episode_length_target"]["max"]:
        errors.append({"code": "INVALID_LENGTH_RANGE", "path": "serialization.episode_length_target", "message": "최소 분량이 최대 분량보다 큽니다."})

    buffer_policy = author_sustainability["buffer_policy"]
    if not (buffer_policy["minimum_launch"] <= buffer_policy["preferred"] <= buffer_policy["deep_buffer"]):
        errors.append({"code": "BUFFER_POLICY_ORDER", "path": "author_sustainability.buffer_policy", "message": "minimum_launch <= preferred <= deep_buffer여야 합니다."})
    if author_sustainability["reaction_check_interval_days"] < 1:
        errors.append({"code": "REACTION_SCHEDULE_MISSING", "path": "author_sustainability.reaction_check_interval_days", "message": "독자 반응 확인 주기가 필요합니다."})
    if serialization["buffer_current"] < serialization["warning_floor"]:
        warnings.append({"code": "BUFFER_WARNING", "path": "serialization.buffer_current", "message": "현재 비축분이 경고선보다 낮습니다."})

    if status in LAUNCH_STATES:
        if serialization["buffer_current"] < serialization["buffer_target"]:
            errors.append({"code": "BUFFER_GATE_FAILED", "path": "serialization.buffer_current", "message": "출시 상태인데 목표 비축분을 충족하지 못했습니다."})
        required_metadata = {
            "title_candidates": bool(metadata["title_candidates"]),
            "short_blurb": _nonempty(metadata["short_blurb"]),
            "long_blurb": _nonempty(metadata["long_blurb"]),
            "tags": bool(metadata["tags"]),
            "age_rating": _nonempty(metadata["age_rating"]),
            "author_notice": _nonempty(metadata["author_notice"]),
        }
        missing_meta = [k for k, ok in required_metadata.items() if not ok]
        if missing_meta:
            errors.append({"code": "LAUNCH_METADATA_MISSING", "path": "metadata", "message": f"출시 메타데이터 누락: {missing_meta}"})
        if risk["ip_review_status"] != "cleared":
            errors.append({"code": "IP_REVIEW_NOT_CLEARED", "path": "risk.ip_review_status", "message": "출시 전 IP 검토가 cleared여야 합니다."})

    status_result = "FAIL" if errors else ("WARN" if warnings else "PASS")
    metrics = {
        "episode_plan_count": len(episodes),
        "buffer_current": serialization["buffer_current"],
        "buffer_target": serialization["buffer_target"],
        "character_count": len(project["characters"]),
        "world_rule_count": len(project["world_rules"]),
        "reaction_check_interval_days": author_sustainability["reaction_check_interval_days"],
    }
    return {"status": status_result, "errors": errors, "warnings": warnings, "metrics": metrics}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("project", type=Path, help="Path to project JSON")
    parser.add_argument("--compact", action="store_true", help="Print compact JSON")
    args = parser.parse_args()

    try:
        project = json.loads(args.project.read_text(encoding="utf-8-sig"))
    except (OSError, json.JSONDecodeError) as exc:
        print(json.dumps({"status": "FAIL", "errors": [{"code": "INPUT", "message": str(exc)}]}, ensure_ascii=False, indent=2))
        return 2

    result = validate_project(project)
    print(json.dumps(result, ensure_ascii=False, indent=None if args.compact else 2))
    return 0 if result["status"] in {"PASS", "WARN"} else 1


if __name__ == "__main__":
    sys.exit(main())

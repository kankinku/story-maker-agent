#!/usr/bin/env python3
"""Audit character-first and episode-engagement fields in a scene contract."""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]


def load(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8-sig"))


def missing_text(container: dict[str, Any], field: str) -> bool:
    value = container.get(field)
    return not isinstance(value, str) or not value.strip()


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("contract", type=Path)
    parser.add_argument("--story-bible", type=Path, required=True, help="Story Bible whose logline and character-first fields must pass.")
    parser.add_argument("--policy", type=Path, default=ROOT / "config" / "engagement_character_policy.json")
    args = parser.parse_args()

    policy = load(args.policy)
    document = load(args.contract)
    issues: list[dict[str, Any]] = []
    if args.story_bible:
        story_bible = load(args.story_bible)
        logline = story_bible.get("logline")
        if not isinstance(logline, dict):
            issues.append({"code": "ENGAGEMENT_LOGLINE_MISSING", "path": "logline"})
        else:
            for field in policy["logline_required_fields"]:
                if missing_text(logline, field):
                    issues.append({"code": "ENGAGEMENT_LOGLINE_FIELD_MISSING", "path": f"logline.{field}"})
        characters = story_bible.get("characters")
        if not isinstance(characters, list) or not characters:
            issues.append({"code": "ENGAGEMENT_CHARACTER_CANON_MISSING", "path": "characters"})
        else:
            for index, character in enumerate(characters):
                base = f"characters[{index}]"
                if not isinstance(character, dict):
                    issues.append({"code": "ENGAGEMENT_CHARACTER_CANON_INVALID", "path": base})
                    continue
                if character.get("engagement_scope") == "supporting_deferred":
                    continue
                for field in policy["character_first_required_fields"]:
                    value = character.get(field)
                    if field == "relationship_variation":
                        if not isinstance(value, list) or not value:
                            issues.append({"code": "ENGAGEMENT_CHARACTER_FIELD_MISSING", "path": f"{base}.{field}"})
                    elif missing_text(character, field):
                        issues.append({"code": "ENGAGEMENT_CHARACTER_FIELD_MISSING", "path": f"{base}.{field}"})
    episode = document.get("episode_contract")
    if not isinstance(episode, dict):
        issues.append({"code": "ENGAGEMENT_EPISODE_CONTRACT_MISSING", "path": "episode_contract"})
        episode = {}
    for field in policy["episode_contract_required_fields"]:
        if missing_text(episode, field):
            issues.append({"code": "ENGAGEMENT_EPISODE_FIELD_MISSING", "path": f"episode_contract.{field}"})

    scenes = document.get("scenes")
    if not isinstance(scenes, list) or not scenes:
        issues.append({"code": "ENGAGEMENT_SCENES_MISSING", "path": "scenes"})
        scenes = []
    allowed = set(policy["allowed_scene_advances"])
    for index, scene in enumerate(scenes):
        base = f"scenes[{index}]"
        if not isinstance(scene, dict):
            issues.append({"code": "ENGAGEMENT_SCENE_INVALID", "path": base})
            continue
        for field in policy["scene_required_fields"]:
            if missing_text(scene, field):
                issues.append({"code": "ENGAGEMENT_SCENE_FIELD_MISSING", "path": f"{base}.{field}"})
        advances = scene.get("advances")
        if not isinstance(advances, list) or not advances:
            issues.append({"code": "ENGAGEMENT_SCENE_NO_ADVANCE", "path": f"{base}.advances"})
        elif any(item not in allowed for item in advances):
            issues.append({"code": "ENGAGEMENT_SCENE_ADVANCE_INVALID", "path": f"{base}.advances"})
        exposition = scene.get("exposition")
        if not isinstance(exposition, dict) or any(missing_text(exposition, key) for key in ["trigger", "immediate_use"]):
            issues.append({"code": "ENGAGEMENT_EXPOSITION_CONTRACT_MISSING", "path": f"{base}.exposition"})

    status = "FAIL" if issues else "PASS"
    result = {"status": status, "errors": issues, "metrics": {"scene_count": len(scenes), "error_count": len(issues)}}
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 1 if issues else 0


if __name__ == "__main__":
    sys.exit(main())

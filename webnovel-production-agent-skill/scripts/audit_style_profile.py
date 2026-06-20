#!/usr/bin/env python3
"""Audit manuscript rhythm and channel structure against a sample style profile."""
from __future__ import annotations

import argparse
import json
import re
import statistics
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]


def read_text(path: Path) -> str:
    for encoding in ("utf-8-sig", "utf-8", "cp949"):
        try:
            return path.read_text(encoding=encoding)
        except UnicodeDecodeError:
            continue
    return path.read_text(encoding="utf-8", errors="replace")


def load_profile(path: Path | None) -> dict[str, Any]:
    if path is None:
        path = ROOT / "templates" / "style_profile.json"
    return json.loads(path.read_text(encoding="utf-8"))


def classify_channel(line: str) -> str:
    stripped = line.strip()
    if not stripped:
        return "blank"
    if re.match(r"^\s*[\[\(<{【].{0,24}(시스템|상태|퀘스트|보상|스킬|알림)", stripped):
        return "system"
    if re.match(r"^\s*(?:[-*]\s*)?(?:ㅇㅇ|익명|분석충|독자|댓글|[A-Za-z0-9가-힣_]{1,12})\s*[:：]", stripped):
        return "community"
    if re.match(r"^\s*[-*]\s*(?:ㅇㅇ|익명|분석충|독자|댓글|[A-Za-z0-9가-힣_]{1,12})\s*[:：]", stripped):
        return "community"
    if re.match(r"^[\"'“‘『「]", stripped) or re.search(r"[\"'”’』」]\s*$", stripped):
        return "dialogue"
    if re.search(r"\b(공격|피했다|휘둘렀|달렸다|붙잡|쓰러|터졌|찔렀|막았|던졌|도망)", stripped):
        return "action"
    return "narration"


def max_streak(values: list[bool]) -> int:
    best = 0
    current = 0
    for value in values:
        if value:
            current += 1
            best = max(best, current)
        else:
            current = 0
    return best


def ending_has_open_loop(lines: list[str]) -> bool:
    tail = " ".join(line.strip() for line in lines[-5:] if line.strip())
    if not tail:
        return False
    patterns = [
        r"\?",
        r"다시\s*(계산|시작|확인|가야|해야)",
        r"(문제|함정|추적|조건|대가|선택|목표|방법|가능성)",
        r"(그 순간|하지만|단,|아직|이제)",
    ]
    return any(re.search(pattern, tail) for pattern in patterns)


def audit(text: str, profile: dict[str, Any]) -> dict[str, Any]:
    issues: list[dict[str, Any]] = []
    raw_lines = text.splitlines()
    lines = [line.rstrip() for line in raw_lines]
    nonempty = [line.strip() for line in lines if line.strip()]
    lengths = [len(line) for line in nonempty]

    rhythm = profile.get("paragraph_rhythm", {})
    median_max = rhythm.get("median_nonempty_line_chars_max", 35)
    short_limit = rhythm.get("short_line_char_limit", 25)
    short_min = rhythm.get("short_line_ratio_min", 0.35)
    long_streak_max = rhythm.get("max_long_line_streak", 3)

    median_len = statistics.median(lengths) if lengths else 0
    short_ratio = (sum(1 for length in lengths if length <= short_limit) / len(lengths)) if lengths else 0
    long_streak = max_streak([len(line) > median_max * 2 for line in nonempty])
    channel_counts: dict[str, int] = {}
    for line in nonempty:
        channel = classify_channel(line)
        channel_counts[channel] = channel_counts.get(channel, 0) + 1
    active_channels = [name for name, count in channel_counts.items() if count > 0]
    open_loop = ending_has_open_loop(nonempty)

    if not nonempty:
        issues.append({"severity": "error", "code": "EMPTY_MANUSCRIPT", "message": "원고에 비어 있지 않은 줄이 없습니다."})
    if median_len > median_max:
        issues.append({
            "severity": "warning",
            "code": "STYLE_LINE_MEDIAN_HIGH",
            "message": f"비어 있지 않은 줄의 중앙 길이 {median_len}자가 프로필 상한 {median_max}자를 넘습니다.",
        })
    if short_ratio < short_min:
        issues.append({
            "severity": "warning",
            "code": "STYLE_SHORT_LINE_RATIO_LOW",
            "message": f"{short_limit}자 이하 줄 비율 {short_ratio:.3f}이 프로필 하한 {short_min:.3f}보다 낮습니다.",
        })
    if long_streak > long_streak_max:
        issues.append({
            "severity": "warning",
            "code": "STYLE_LONG_LINE_STREAK",
            "message": f"긴 줄이 {long_streak}개 연속됩니다. 상한은 {long_streak_max}개입니다.",
        })
    if len(active_channels) < 2 and len(nonempty) >= 8:
        issues.append({
            "severity": "warning",
            "code": "STYLE_CHANNEL_MONOTONY",
            "message": "충분히 긴 원고인데 정보 채널이 한 종류에 가깝습니다.",
        })
    if len(nonempty) >= 8 and not open_loop:
        issues.append({
            "severity": "warning",
            "code": "STYLE_NO_ENDING_OPEN_LOOP",
            "message": "말미에 다음 행동을 강제하는 정보, 비용, 질문, 선택지가 약합니다.",
        })

    errors = [issue for issue in issues if issue["severity"] == "error"]
    warnings = [issue for issue in issues if issue["severity"] == "warning"]
    return {
        "status": "FAIL" if errors else ("WARN" if warnings else "PASS"),
        "profile_id": profile.get("profile_id", ""),
        "metrics": {
            "nonempty_line_count": len(nonempty),
            "median_nonempty_line_chars": median_len,
            "short_line_char_limit": short_limit,
            "short_line_ratio": round(short_ratio, 3),
            "max_long_line_streak": long_streak,
            "channel_counts": channel_counts,
            "active_channel_count": len(active_channels),
            "ending_open_loop": open_loop,
        },
        "errors": errors,
        "warnings": warnings,
        "policy": "Warnings are revision targets; hard failure is reserved for empty or unreadable manuscripts.",
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("manuscript", type=Path)
    parser.add_argument("--profile", type=Path, default=None)
    parser.add_argument("--fail-on-warn", action="store_true")
    args = parser.parse_args()

    text = read_text(args.manuscript)
    result = audit(text, load_profile(args.profile))
    print(json.dumps(result, ensure_ascii=False, indent=2))
    if result["status"] == "FAIL":
        return 1
    if args.fail_on_warn and result["status"] == "WARN":
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())

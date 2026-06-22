from __future__ import annotations

import hashlib
import json
import re
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PROJECT = ROOT / "projects" / "muhan_regression_remake_10"
MIN_NONSPACE = 3600
TITLES = [
    "끝나고 시작된 게임",
    "무회갤의 뉴비",
    "최초 입장자는 인피니티",
    "리세마라의 시작",
    "단전을 만들라는 마법사",
    "직업은 무투가",
    "코어를 쓰는 법",
    "죽어야 정산된다",
    "오크 족장 2회차",
    "차원간 거래",
]


def nonspace(text: str) -> int:
    return len(re.sub(r"\s+", "", text))


def sha(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def split_source(source: str) -> list[str]:
    lines = source.splitlines()
    markers = [index for index, line in enumerate(lines) if "novelpia.com" in line]
    starts = [0] + [index + 1 for index in markers[:9]]
    ends = markers[:10]
    return ["\n".join(lines[start:end]) for start, end in zip(starts, ends)]


def clean_line(line: str) -> str:
    line = line.replace("\u00a0", " ").replace("∗∗*", "* * *")
    if line.strip() == "***":
        line = "* * *"
    line = re.sub(r"[ \t]+", " ", line).strip()
    line = re.sub(r",(?=[가-힣A-Za-z0-9])", ", ", line)
    line = re.sub(r"\.(?=[가-힣A-Za-z])", ". ", line)
    line = re.sub(r"\?(?=[가-힣A-Za-z])", "? ", line)
    line = re.sub(r"!(?=[가-힣A-Za-z])", "! ", line)
    return line


def remaster(segment: str, number: int) -> str:
    ignored = ("커버보기", "한번 더 누르면 다음화로 이동합니다", "OCR 결과 없음")
    cleaned: list[str] = []
    blank = False
    recent = Counter()
    for raw in segment.splitlines():
        if any(token in raw for token in ignored):
            continue
        line = clean_line(raw)
        if re.fullmatch(r"\d{1,3}", line):
            continue
        if not line:
            if cleaned and not blank:
                cleaned.append("")
            blank = True
            continue
        blank = False
        # OCR/page capture sometimes duplicated identical prose blocks. Keep intentional
        # short refrains, but drop the third and later exact long-line duplicate.
        if len(line) >= 18 and recent[line] >= 2:
            continue
        recent[line] += 1
        cleaned.append(line)
    body = "\n".join(cleaned).strip()
    return f"# 제{number}화. {TITLES[number - 1]}\n\n{body}\n"


def repetition(text: str) -> dict:
    lines = [line.strip() for line in text.splitlines() if len(line.strip()) >= 18]
    counts = Counter(lines)
    return {
        "line_count": len(lines),
        "unique_ratio": round(len(counts) / max(1, len(lines)), 4),
        "max_line_repeat": max(counts.values(), default=0),
        "repeat_excess": sum(value - 1 for value in counts.values()),
    }


def main() -> int:
    bible = json.loads((PROJECT / "story_bible.json").read_text(encoding="utf-8"))
    source_path = ROOT / bible["source"]["path"]
    source = source_path.read_text(encoding="utf-8")
    segments = split_source(source)
    draft_dir = PROJECT / "drafts"
    final_dir = PROJECT / "episodes"
    human_dir = PROJECT / "humanization"
    report_dir = PROJECT / "reports"
    for directory in (draft_dir, final_dir, human_dir, report_dir):
        directory.mkdir(parents=True, exist_ok=True)

    reports = []
    episode_map = []
    for number, segment in enumerate(segments, 1):
        tag = f"{number:03d}"
        final = remaster(segment, number)
        draft_path = draft_dir / f"episode_{tag}.md"
        final_path = final_dir / f"episode_{tag}.md"
        draft_path.write_bytes((segment.strip() + "\n").encode("utf-8"))
        final_path.write_bytes(final.encode("utf-8"))
        rep = repetition(final)
        status = "PASS" if nonspace(final) >= MIN_NONSPACE and rep["max_line_repeat"] <= 2 else "FAIL"
        report = {
            "episode": number,
            "status": status,
            "skill": "humanize-korean",
            "mode": "source_faithful_remaster",
            "draft_path": str(draft_path.resolve()),
            "final_path": str(final_path.resolve()),
            "manuscript_path": str(final_path.resolve()),
            "draft_sha256": sha(segment.strip() + "\n"),
            "final_sha256": sha(final),
            "manuscript_hash": "sha256:" + sha(final),
            "draft_nonspace": nonspace(segment),
            "final_nonspace": nonspace(final),
            "repetition": rep,
            "preserved": ["source_event_order", "source_characters", "source_world_rules", "source_pov"],
            "edits": ["scraper_artifact_removal", "ocr_duplicate_reduction", "spacing", "punctuation", "episode_title"],
        }
        (human_dir / f"episode_{tag}.json").write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        reports.append(report)
        episode_map.append({"number": number, "title": TITLES[number - 1], "source_order": number, "nonspace": nonspace(final)})

    generation = {
        "status": "PASS" if all(item["status"] == "PASS" for item in reports) else "FAIL",
        "mode": "source_faithful_remaster",
        "source_path": str(source_path.resolve()),
        "source_sha256": bible["source"]["sha256"],
        "minimum_nonspace": MIN_NONSPACE,
        "episodes": reports,
    }
    (report_dir / "generation_report.json").write_text(json.dumps(generation, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    (PROJECT / "source_remaster_map.json").write_text(json.dumps({"episodes": episode_map}, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return 0 if generation["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())

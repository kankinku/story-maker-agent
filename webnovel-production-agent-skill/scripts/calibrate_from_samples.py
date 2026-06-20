#!/usr/bin/env python3
"""Derive lexicon and voice candidates from supplied Korean webnovel TXT samples."""
from __future__ import annotations

import argparse
import json
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any, Iterable

ROOT = Path(__file__).resolve().parents[1]

STOPWORDS = {
    "그리고",
    "그러나",
    "하지만",
    "그는",
    "그녀는",
    "나는",
    "내가",
    "것은",
    "것이",
    "있었다",
    "없었다",
    "했다",
    "된다",
    "하는",
    "에서",
    "으로",
    "에게",
}

TERM_HINTS = {
    "상태창",
    "시스템",
    "스킬",
    "특성",
    "던전",
    "게이트",
    "회귀",
    "아카데미",
    "헌터",
    "마력",
    "랭킹",
    "보상",
    "퀘스트",
    "각성",
    "교관",
    "길드",
}


def read_text(path: Path) -> str:
    for encoding in ("utf-8-sig", "utf-8", "cp949"):
        try:
            return path.read_text(encoding=encoding)
        except UnicodeDecodeError:
            continue
    return path.read_text(encoding="utf-8", errors="replace")


def format_sample_path(path: Path, mode: str) -> str:
    if mode == "absolute":
        return str(path)
    if mode == "relative":
        return str(path.relative_to(ROOT)) if path.is_relative_to(ROOT) else path.name
    return path.name


def collect_sample_paths(inputs: list[Path]) -> list[Path]:
    paths: list[Path] = []
    for item in inputs:
        if item.is_dir():
            paths.extend(sorted(path for path in item.rglob("*") if path.suffix.lower() in {".txt", ".md"}))
        elif item.suffix.lower() in {".txt", ".md"}:
            paths.append(item)
    return sorted(dict.fromkeys(path.resolve() for path in paths))


def infer_source_tags(path: Path) -> dict[str, str]:
    stem = path.stem
    parts = [part for part in re.split(r"[-_]", stem) if part]
    return {
        "platform": parts[0] if len(parts) >= 1 else "",
        "genre": parts[1] if len(parts) >= 2 else "",
        "label": "-".join(parts[2:]) if len(parts) >= 3 else stem,
    }


def korean_tokens(text: str) -> list[str]:
    tokens = re.findall(r"[가-힣A-Za-z0-9]{2,}", text)
    normalized = [normalize_token(token) for token in tokens]
    return [token for token in normalized if len(token) >= 2 and token not in STOPWORDS and not token.isdigit()]


def normalize_token(token: str) -> str:
    if not re.fullmatch(r"[가-힣]+", token):
        return token
    for suffix in ["으로부터", "에게서", "에서는", "에게는", "까지", "부터", "보다", "에게", "께서", "에서", "으로", "로서", "로써", "만큼", "처럼", "조차", "마저", "마다", "하고", "이며", "이고", "은", "는", "이", "가", "을", "를", "에", "로", "와", "과", "도", "만", "의"]:
        if token.endswith(suffix) and len(token) - len(suffix) >= 2:
            return token[:-len(suffix)]
    return token


def sentence_endings(text: str) -> Counter[str]:
    endings: Counter[str] = Counter()
    for sentence in re.split(r"[.!?。！？\n]+", text):
        stripped = sentence.strip()
        if not stripped:
            continue
        cleaned = re.sub(r"[\s\"'“”‘’.,!?。！？]+$", "", stripped)
        hangul = re.findall(r"[가-힣]{2,8}$", cleaned)
        if hangul:
            endings[hangul[-1][-6:]] += 1
    return endings


def dialogue_spans(text: str) -> list[str]:
    spans = re.findall(r'"([^"\n]{1,120})"|“([^”\n]{1,120})”|‘([^’\n]{1,120})’', text)
    return [next(part for part in match if part) for match in spans if any(match)]


def remove_dialogue(text: str) -> str:
    return re.sub(r'"[^"\n]{1,120}"|“[^”\n]{1,120}”|‘[^’\n]{1,120}’', " ", text)


def line_structure_metrics(text: str) -> dict[str, Any]:
    lines = [line.strip() for line in text.splitlines() if line.strip()]
    lengths = [len(line) for line in lines]
    if not lengths:
        return {
            "nonempty_line_count": 0,
            "median_line_chars": 0,
            "short_line_ratio_25": 0.0,
            "system_like_line_count": 0,
            "community_like_line_count": 0,
            "dialogue_line_count": 0,
        }
    system_like = sum(1 for line in lines if re.match(r"^[\[\(<{【].{0,24}(시스템|상태|퀘스트|보상|스킬|알림)", line))
    community_like = sum(1 for line in lines if re.match(r"^(?:[-*]\s*)?(?:ㅇㅇ|익명|분석충|독자|댓글|[A-Za-z0-9가-힣_]{1,12})\s*[:：]", line))
    dialogue_like = sum(1 for line in lines if re.match(r"^[\"'“‘『「]", line) or re.search(r"[\"'”’』」]\s*$", line))
    sorted_lengths = sorted(lengths)
    mid = len(sorted_lengths) // 2
    if len(sorted_lengths) % 2:
        median = sorted_lengths[mid]
    else:
        median = (sorted_lengths[mid - 1] + sorted_lengths[mid]) / 2
    return {
        "nonempty_line_count": len(lines),
        "median_line_chars": median,
        "short_line_ratio_25": round(sum(1 for length in lengths if length <= 25) / len(lengths), 3),
        "system_like_line_count": system_like,
        "community_like_line_count": community_like,
        "dialogue_line_count": dialogue_like,
    }


def load_phrase_rules(paths: Iterable[Path]) -> list[dict[str, Any]]:
    rules: list[dict[str, Any]] = []
    for path in paths:
        doc = json.loads(path.read_text(encoding="utf-8"))
        for entry in doc.get("entries", []):
            if entry.get("kind") in {"ai_tell_phrase", "prohibited_phrase"}:
                rule = dict(entry)
                rule["_source"] = path.name
                rules.append(rule)
    return rules


def count_rule(text: str, surface: str, match_type: str) -> int:
    if match_type == "regex":
        return len(re.findall(surface, text))
    if match_type == "exact":
        return sum(1 for token in re.findall(r"\S+", text) if token.strip(".,!?\"'“”‘’()[]{}") == surface)
    if match_type == "document_metric":
        return 0
    return text.count(surface)


def candidate_entry(entry_id: str, surface: str, kind: str, category: str, count: int, docs: list[str]) -> dict[str, Any]:
    return {
        "id": entry_id,
        "surface": surface,
        "kind": kind,
        "category": category,
        "count": count,
        "document_count": len(set(docs)),
        "documents": sorted(set(docs)),
        "review_status": "candidate",
        "sample_dependency": True,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("samples", nargs="+", type=Path, help="Sample TXT/MD files or directories.")
    parser.add_argument("--output", type=Path, default=ROOT / "sample_calibration_report.json")
    parser.add_argument("--top", type=int, default=30)
    parser.add_argument("--min-count", type=int, default=2)
    parser.add_argument("--lexicon-dir", type=Path, default=ROOT / "lexicons")
    parser.add_argument(
        "--path-mode",
        choices=["basename", "relative", "absolute"],
        default="basename",
        help="How sample paths are stored in the derived report. Use basename for portable reports.",
    )
    args = parser.parse_args()

    sample_paths = collect_sample_paths(args.samples)
    if not sample_paths:
        print(json.dumps({"status": "FAIL", "error": "NO_SAMPLE_FILES"}, ensure_ascii=False, indent=2))
        return 1

    token_counts: Counter[str] = Counter()
    token_docs: dict[str, list[str]] = defaultdict(list)
    term_counts: Counter[str] = Counter()
    term_docs: dict[str, list[str]] = defaultdict(list)
    ending_counts: Counter[str] = Counter()
    dialogue_ending_counts: Counter[str] = Counter()
    per_sample: list[dict[str, Any]] = []
    phrase_hits: list[dict[str, Any]] = []
    structure_summaries: list[dict[str, Any]] = []
    phrase_rules = load_phrase_rules([
        args.lexicon_dir / "ai_tell_phrases.ko.json",
        args.lexicon_dir / "prohibited_phrases.ko.json",
    ])

    for path in sample_paths:
        text = read_text(path)
        tags = infer_source_tags(path)
        rel = format_sample_path(path, args.path_mode)
        tokens = korean_tokens(text)
        structure = line_structure_metrics(text)
        structure_summaries.append({"path": rel, **structure})
        local_counts = Counter(tokens)
        for token, count in local_counts.items():
            token_counts[token] += count
            token_docs[token].append(rel)
            if token in TERM_HINTS or any(hint in token for hint in TERM_HINTS):
                term_counts[token] += count
                term_docs[token].append(rel)
        endings = sentence_endings(remove_dialogue(text))
        ending_counts.update(endings)
        dialogue_endings = Counter()
        for span in dialogue_spans(text):
            dialogue_endings.update(sentence_endings(span))
        dialogue_ending_counts.update(dialogue_endings)
        local_phrase_hits = []
        for rule in phrase_rules:
            count = count_rule(text, rule["surface"], rule.get("match_type", "substring"))
            if count:
                hit = {
                    "id": rule["id"],
                    "surface": rule["surface"],
                    "kind": rule["kind"],
                    "category": rule.get("category", ""),
                    "severity": rule.get("severity", "info"),
                    "count": count,
                    "threshold": rule.get("threshold", 1),
                    "source": rule["_source"],
                    "sample": rel,
                    "review_action": "calibrate_false_positive_or_keep_blocker",
                }
                local_phrase_hits.append(hit)
                phrase_hits.append(hit)
        per_sample.append({
            "path": rel,
            "platform": tags["platform"],
            "genre": tags["genre"],
            "label": tags["label"],
            "characters": len(text),
            "token_count": len(tokens),
            "dialogue_line_count": len(dialogue_spans(text)),
            "style_structure": structure,
            "ai_tell_or_prohibited_hits": len(local_phrase_hits),
        })

    term_candidates = [
        candidate_entry(
            f"sample_term_{idx:03d}",
            surface,
            "webnovel_term" if surface in TERM_HINTS else "genre_term",
            "sample_frequency",
            count,
            term_docs[surface],
        )
        for idx, (surface, count) in enumerate(term_counts.most_common(args.top), start=1)
        if count >= 1
    ]
    high_frequency_candidates = [
        candidate_entry(
            f"sample_freq_{idx:03d}",
            surface,
            "genre_term",
            "high_frequency",
            count,
            token_docs[surface],
        )
        for idx, (surface, count) in enumerate(token_counts.most_common(args.top), start=1)
        if count >= args.min_count
    ]
    voice_candidates = [
        {
            "ending": ending,
            "count": count,
            "kind": "narration_ending" if source == "narration" else "dialogue_ending",
            "review_status": "candidate",
            "sample_dependency": True,
        }
        for source, counter in [("narration", ending_counts), ("dialogue", dialogue_ending_counts)]
        for ending, count in counter.most_common(args.top)
        if count >= 1
    ]

    result = {
        "status": "PASS",
        "sample_count": len(sample_paths),
        "samples": per_sample,
        "lexicon_candidates": {
            "term_candidates": term_candidates,
            "high_frequency_candidates": high_frequency_candidates,
            "voice_candidates": voice_candidates,
        },
        "im_not_ai_alignment": {
            "rules_checked": len(phrase_rules),
            "sample_phrase_hits": phrase_hits,
            "policy": "Promote sample-backed new rules only after at least two evidence spans; downgrade false positives caused by normal webnovel grammar."
        },
        "style_structure_candidates": {
            "policy": "Use these as draft thresholds for templates/style_profile.json; do not store or quote source prose.",
            "per_sample": structure_summaries,
        },
        "copyright_policy": "Output stores derived terms, counts, endings, and rule ids only; it does not copy source prose.",
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())

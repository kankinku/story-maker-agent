# Sample-Driven Improvement Plan

Date: 2026-06-16

## User Direction

1. Webnovel dictionary and 3. character voice dictionary will be calibrated from current popular webnovel TXT samples supplied by the user.
2. Prohibited and AI-tell phrase improvement will be based on the local `im-not-ai` repository, then adjusted with the same samples.
3. Remaining missing components need an implementation plan.

## Implemented Now

- Added `lexicons/` as a first-class skill resource.
- Added `schemas/lexicon.schema.json`.
- Added starter webnovel, genre, platform, AI-tell, prohibited phrase, and character voice lexicons.
- Added `scripts/audit_lexicon.py`.
- Added `scripts/calibrate_from_samples.py`.
- Added clean and noisy manuscript fixtures.
- Integrated lexicon validation and sample calibration smoke checks into the generated test report.
- Ingested group_01 samples supplied by the user on 2026-06-16.
- Added `reports/group_01_sample_calibration.json` with derived terms, endings, and im-not-ai hits only.
- Added `lexicons/sample_group_01_terms.ko.json` and `lexicons/sample_group_01_voice.ko.json`.
- Added `reports/group_01_im_not_ai_alignment.json` and calibrated common grammar-like im-not-ai hits from S1 blockers to S2 density warnings where justified.

## Sample Intake Contract

Place supplied TXT files under a future sample folder such as:

```text
samples/
  popular/
    {platform}-{genre}-{rank-or-title}.txt
```

For each sample, extract:

- high-frequency genre nouns
- coined terms and system/UI terms
- platform/tag words
- repeated sentence endings
- dialogue endings by character
- internal monologue markers
- AI-tell overlap and false positives

Do not copy protected prose into reusable outputs. Store only short terms, counts, categories, and derived rules.

## Item 1 - Webnovel Dictionary

Current state: scaffolded as `lexicons/webnovel_terms.ko.json`, `genre_terms.ko.json`, and `platform_keywords.ko.json`; group_01 sample-backed additions live in `lexicons/sample_group_01_terms.ko.json`.

Next after more samples:

1. Compute term frequency by genre/platform.
2. Mark overused generic terms versus genre-standard terms.
3. Split terms into `allowed_contexts` and `avoid_contexts`.
4. Connect terms to episode `new_terms` and exposition budget.
5. Add unknown high-frequency coined-term reporting.

Command:

```bash
python scripts/calibrate_from_samples.py samples/popular --output sample_calibration_report.json
```

## Item 2 - im-not-ai Based AI-Tell/Prohibited Phrase Layer

Current state: seeded as `lexicons/ai_tell_phrases.ko.json` and `prohibited_phrases.ko.json`; group_01 alignment is recorded in `reports/group_01_im_not_ai_alignment.json`.

Basis used:

- im-not-ai AI-tell categories A-J
- quick-rules severity model S1/S2/S3
- fidelity-first and no-over-polish rules
- 30% warning / 50% stop-or-rollback rewrite-rate policy

Next after more samples:

1. Run `calibrate_from_samples.py` on the sample directory and `audit_lexicon.py --manuscript` on generated drafts.
2. Label false positives caused by normal webnovel grammar.
3. Promote repeated sample-backed findings to active rules only after at least two evidence spans.
4. Keep S1 rules strict; keep sample-sensitive S2 rules as calibrated thresholds.

## Item 3 - Character Voice Dictionary

Current state: scaffolded as `lexicons/character_voice.template.json`; corpus-level group_01 voice markers live in `lexicons/sample_group_01_voice.ko.json`.

Next after more samples:

1. Split dialogue and internal monologue by character using the sample calibration report as the first rough pass.
2. Extract preferred endings, avoided endings, habitual verbs, address terms, honorific targets, and emotional leakage patterns.
3. Convert `characters[].speech_marker` from a single string into a checked voice profile.
4. Add manuscript audit for character-specific register drift.

## Remaining Improvement Plan

Priority order:

1. `scripts/check_platform_freshness.py`: warn when platform profiles are stale and require browse-backed refresh for launch metadata.
2. `scripts/audit_rewrite_fidelity.py`: compare source and rewrite for missing events, invented events, reordered beats, named-entity drift, and direct-quote drift.
3. `scripts/run_semantic_rubric.py`: produce human-reviewable 1-5 scores from `evaluation_policy.json`.
4. Real `.omx` hook runtime: move prompt-level hook routing into executable prompt classification/state injection.
5. Done: `scripts/calibrate_from_samples.py`: derive lexicon candidates from supplied TXT without storing copyrighted prose.

## Acceptance Criteria For Remaining Items

### Platform Freshness Checker

- Input: `config/platform_profiles.json`.
- Output: JSON status with stale platforms, `last_verified`, and required refresh action.
- Exit: warn or fail when launch metadata depends on platform facts older than the configured threshold.

### Rewrite Fidelity Checker

- Input: source outline/text and rewritten output.
- Output: missing events, invented events, reordered beats, named-entity drift, direct-quote drift.
- Exit: fail on structural drift before style polishing or manuscript guard.

### Semantic Rubric Runner

- Input: manuscript/plan plus `config/evaluation_policy.json`.
- Output: 1-5 score table with evidence fields and human-review notes.
- Exit: no automatic launch approval; scores become review evidence only.

### Real OMX Hook Runtime

- Input: user prompt and `.omx/state/webnovel-production-workflow.json`.
- Output: intent, phase, selected loop, required checks, and state transition.
- Exit: hook output matches prompt-level routing on fixture prompts.

## Current Limitation

The lexicon layer is now sample-calibrated for group_01, but still lacks platform/rank metadata and character speaker labels. The next useful improvement is a length-normalized AI-tell density auditor plus character-specific dialogue attribution.

# Skill Needs Assessment

Date: 2026-06-16

Scope:

- `.codex/`
- `webnovel-production-agent-skill/`
- `AGENTS.md`
- `SKILL_AUDIT_REPORT.md`

## Current Status

The project now has a portable skill package structure:

- project `AGENTS.md`
- Codex local workflow skill
- Hyperagent-style package export
- manifests
- input/output schemas
- deterministic validators
- regression fixtures
- generated test report
- manuscript guard wrapper
- workflow state writer
- checksum audit
- lexicon schema
- starter webnovel/genre/platform dictionaries
- im-not-ai seeded AI-tell and prohibited phrase dictionaries
- character voice dictionary template
- lexicon audit script
- sample calibration script

Current automated audit:

- `audit_skill_package.py`: PASS
- `validate_project.py`: PASS
- `audit_narrative.py`: PASS
- `run_regression.py`: 6 passed, 0 failed
- `generate_test_report.py`: PASS
- manuscript guard smoke: PASS
- `audit_lexicon.py`: PASS
- `calibrate_from_samples.py`: PASS on fixture sample corpus

## Inventory Result

### Present

- routing metadata
- when-to-use and when-not-to-use rules
- control-loop workflow
- phase and iteration state shape
- story bible and project schema
- episode planning fields
- `new_terms` per episode
- exposition budget validation
- speech marker per character
- sentence assembly guidance
- AI-tell guard wrapper
- package-level audit

### Missing Or Weak After Lexicon Scaffold

- sample-calibrated webnovel lexicon/glossary
- sample-calibrated allowed/forbidden vocabulary lists
- sample-calibrated genre-specific term bank
- sample-calibrated platform keyword dictionary
- filled character voice dictionary per named character
- recurring phrase and overused expression detector beyond seeded phrases
- sample-derived candidate review and promotion workflow for real popular TXT samples
- honorific/register consistency checker
- style sample calibration fixture
- source-faithfulness checker for rewrite workflows
- real OMX `UserPromptSubmit` hook implementation
- semantic evaluator for the 1-5 rubric
- stale platform profile checker
- dictionary-backed metadata/tag generator

## Webnovel Dictionary Necessity Test

### Test Question

Does the current system have enough structure to control webnovel vocabulary, genre terms, character voice, platform tags, and repeated expressions across long serialization?

### Evidence

The current package has:

- `plot.episodes[].new_terms`
- `narrative_engine.exposition_policy.max_new_terms_per_episode`
- character `speech_marker`
- metadata `tags`
- sentence assembly instructions

But it does not have:

- a canonical dictionary file
- a schema for dictionary entries
- a validator that checks manuscript vocabulary against the dictionary
- a forbidden or overused phrase list
- character-specific vocabulary/register rules
- platform tag/keyword normalization
- genre trope term bank

### Result

`NEEDED - SCAFFOLD IMPLEMENTED`

A webnovel dictionary is necessary because the current `new_terms` field only controls episode-level information load. A first lexicon layer now exists, but it still needs the user's current popular webnovel TXT samples for frequency, genre, platform, and character voice calibration.

## Recommended Dictionary Structure

Added:

```text
webnovel-production-agent-skill/
├── lexicons/
│   ├── webnovel_terms.ko.json
│   ├── genre_terms.ko.json
│   ├── platform_keywords.ko.json
│   ├── prohibited_phrases.ko.json
│   ├── ai_tell_phrases.ko.json
│   └── character_voice.template.json
├── schemas/
│   └── lexicon.schema.json
├── scripts/
│   └── audit_lexicon.py
└── tests/
    └── fixtures/
        ├── valid_lexicon.json
        ├── invalid_lexicon.json
        ├── manuscript_with_repetition.txt
        └── manuscript_clean_sample.txt
```

## Proposed Lexicon Entry

```json
{
  "id": "term_status_window",
  "surface": "상태창",
  "category": "system_ui",
  "genres": ["현대판타지", "게임판타지"],
  "allowed_contexts": ["system_message", "protagonist_observation"],
  "avoid_contexts": ["romance_emotional_peak"],
  "synonyms": ["시스템창", "알림창"],
  "register": "genre_standard",
  "notes": "반복 사용 시 상태창 자체보다 선택과 비용을 강조한다."
}
```

## Needed Validators

### 1. Lexicon Schema Validation

Checks:

- required ids
- duplicate surface forms
- category enum
- genre compatibility
- synonym cycles

### 2. Manuscript Lexicon Audit

Checks:

- prohibited phrase occurrence
- repeated phrase over threshold
- unknown high-frequency coined terms
- character voice rule violations
- honorific/register inconsistency
- platform tag mismatch
- AI-tell phrase overlap

### 3. Episode Term Continuity

Checks:

- terms introduced in `new_terms` are reused consistently
- hidden terms are not explained before reveal
- reminder required for long-unused coined terms
- exposition budget is dictionary-aware, not only count-based

## Priority List

### P0

1. Done: add `lexicon.schema.json`.
2. Done: add `lexicons/webnovel_terms.ko.json`.
3. Done: add `lexicons/prohibited_phrases.ko.json`.
4. Done: add `lexicons/ai_tell_phrases.ko.json`.
5. Done: add `audit_lexicon.py`.
6. Done: add clean/repetition manuscript fixtures.
7. Done: include lexicon audit in `generate_test_report.py`.
8. Ready: `calibrate_from_samples.py` can derive candidates once user-supplied current popular webnovel TXT samples are present.

### P1

1. Done: add `character_voice.template.json`.
2. Pending: connect character `speech_marker` to character voice dictionary after sample-derived voice candidates are reviewed.
3. Pending: add honorific/register consistency checks.
4. Pending: add platform keyword normalization.
5. Partial: add genre-specific starter term bank by major genre; sample calibration still needed.

### P2

1. Add style sample calibration.
2. Add corpus-derived overused expression threshold.
3. Add rewrite source-faithfulness checker.
4. Add real OMX hook implementation.
5. Add semantic rubric runner for 1-5 scoring.

## Other Missing Components

### Real Hook Runtime

Current hook routing is prompt-level. It should eventually become a real runtime hook that:

- classifies the user prompt
- reads `.omx/state`
- injects active phase
- records state transitions

### Platform Freshness Checker

`platform_profiles.json` has `last_verified`, but no script fails or warns when it is stale.

Needed:

- `scripts/check_platform_freshness.py`

### Semantic Rubric Runner

`evaluation_policy.json` defines a 1-5 rubric, but no runner produces the score.

Needed:

- `scripts/run_semantic_rubric.py`
- human-review compatible JSON output

### Rewrite Fidelity Checker

Memory and prior workflow require structure-preserving rewrites, but this package does not yet include a checker for:

- missing events
- invented events
- reordered events
- named entity drift
- direct quote drift

Needed:

- `scripts/audit_rewrite_fidelity.py`

## Next Recommended Implementation Order

1. Build the lexicon layer first.
2. Add `audit_lexicon.py` to the generated test report.
3. Add platform freshness check.
4. Add rewrite fidelity check.
5. Add semantic rubric runner.
6. Only then consider real OMX hook code.

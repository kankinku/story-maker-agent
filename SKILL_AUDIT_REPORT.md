# Skill Audit Report

Date: 2026-06-16

Scope:

- `.codex/skills/webnovel-production-workflow`
- `webnovel-production-agent-skill`

Reference standard:

- Hyperagent-style portable skill package fields:
  `metadata`, `routing`, `documentation`, `skillMdBody`, `tags`, `scripts`, `references`, `manifest`, `input/output schema`, `permissions`, `validation`, and deterministic checks.

## Inventory

| Skill | Type | Status | Notes |
|---|---|---|---|
| `webnovel-production-loop` | Hyperagent-style export package | Improved | Added manifest, input/output schemas, package audit script, guard runner, workflow state runner, generated test report, checksums, lexicon audit layer, sample calibration smoke, and 1.7.0 metadata. |
| `webnovel-production-workflow` | Codex project-local workflow skill | Improved | Added manifest with routing, validators, permissions, and control-loop declarations. |

## Improvements Applied

### 1. Portable Manifest

Added:

- `webnovel-production-agent-skill/manifest.json`
- `.codex/skills/webnovel-production-workflow/manifest.json`

These define:

- skill id and version
- routing rules
- when-to-use / when-not-to-use
- example triggers
- entrypoint
- permissions
- validators
- human approval boundaries

### 2. Input And Output Schemas

Added:

- `webnovel-production-agent-skill/schemas/input.schema.json`
- `webnovel-production-agent-skill/schemas/output.schema.json`

The workflow now has a machine-readable contract for:

- intent classification
- project/manuscript/metrics/failure inputs
- phase result
- artifacts
- validation results
- blocked status and next action

### 3. Full Skill Audit Script

Added:

- `webnovel-production-agent-skill/scripts/audit_skill_package.py`

The script checks:

- required package files
- metadata keys
- manifest keys
- version drift
- bundle document existence
- reference target status
- script descriptions
- Hyperagent export shape
- nested JSON string parseability for `tags` and `scripts`
- `documentation` and `skillMdBody` sync
- bundle documents included in export
- Codex local skill manifests and routing completeness

### 4. Export Improvements

Updated:

- `metadata.json`
- `dist/webnovel-production-loop.skill.json`

The export now includes:

- bundled `manifest.json`
- bundled `SENTENCE_ASSEMBLY_SYSTEM.md`
- `audit_skill_package.py` in exported scripts
- parseable nested `tags`
- parseable nested `scripts`

### 5. Version And Documentation

Updated package version:

- `1.7.0`

Updated:

- `README.md`
- `CHANGELOG.md`
- `TEST_REPORT.json`

### 6. Runtime Automation

Added:

- `run_manuscript_guard.py`: blocks completion until `$humanize-korean` is confirmed and `ai_tell_guard.py --fail-on-s1` can run or is explicitly unavailable.
- `workflow_state.py`: reads/writes `.omx/state/webnovel-production-workflow.json`.
- `generate_test_report.py`: regenerates `TEST_REPORT.json` from actual commands.
- `update_manifest_checksums.py`: populates `sha256` for manifest assets and scripts.
- schema fixtures for valid/invalid input and output contracts.
- `audit_lexicon.py`: validates lexicon files and audits manuscripts for AI-tell/prohibited phrase hits.
- `calibrate_from_samples.py`: derives lexicon, voice, and im-not-ai alignment candidates from supplied TXT/MD samples without storing source prose.
- `lexicons/*.json`: starter webnovel, genre, platform, AI-tell, prohibited phrase, and character voice dictionaries.

## Current Verification

Commands run from `webnovel-production-agent-skill/`:

```powershell
python scripts/build_export.py --output dist/webnovel-production-loop.skill.json
python scripts/generate_test_report.py --project-root ..
python scripts/audit_skill_package.py --project-root ..
python scripts/validate_project.py tests/fixtures/valid_project.json --compact
python scripts/audit_narrative.py tests/fixtures/valid_project.json
python scripts/audit_lexicon.py
python scripts/calibrate_from_samples.py tests/fixtures/sample_corpus --output tests/fixtures/sample_calibration_report.json
python scripts/run_regression.py tests/regression_cases.json
```

Results:

- package audit: `PASS`, 0 errors, 0 warnings
- project validator: `PASS`
- narrative audit: `PASS`
- lexicon audit: `PASS`
- sample calibration smoke: `PASS`
- regression: `6 passed`, `0 failed`
- generated test report: `PASS`
- manuscript guard smoke test: `PASS`

## Remaining Improvement Candidates

- Add a stricter export schema validator if the target importer rejects unknown data keys or optional references.
- Add a real OMX hook implementation if this workspace later uses OMX runtime hooks directly.

# Sample Fourfold Text File Inspection

Date: 2026-06-17

## 1. Original Sample TXT Availability

Current workspace scan for `*.txt` did not find the four original sample files at the workspace root or a `samples/` folder.

Available evidence for the four original samples is the existing agent-system output:

- `webnovel-production-agent-skill/reports/group_01_sample_calibration.json`
- status: `PASS`
- sample_count: `4`

Recorded samples:

| Sample | Characters | Tokens | Dialogue Lines | AI/Prohibited Hits |
|---|---:|---:|---:|---:|
| `무한회귀.txt` | 320508 | 67012 | 1151 | 8 |
| `차원이동.txt` | 170160 | 36846 | 361 | 6 |
| `초월자갤러리.txt` | 958174 | 200100 | 2016 | 8 |
| `흡혈귀.txt` | 407137 | 86035 | 1156 | 7 |

Conclusion: direct re-read of original TXT files is unavailable in the current workspace, but the prior calibration artifact proves the agent system processed four supplied TXT samples.

## 2. Generated Draft File Checks

Core invariants checked in each generated file:

- protagonist: `이민재`
- location: `남구`
- ability: `피의 문`
- community device: `문밖 게시판`
- predecessor clue: `전임자`
- mystery actor class: `접속자`
- long-term target: `고정자`
- three episode headings

| Draft | Characters | No-Space Characters | Episode Headings | Missing Core Terms |
|---|---:|---:|---:|---|
| `drafts/sample_fourfold_muhan_regression_episodes_1_3.md` | 4559 | 3263 | 3 | none |
| `drafts/sample_fourfold_dimension_transfer_episodes_1_3.md` | 3641 | 2605 | 3 | none |
| `drafts/sample_fourfold_transcendent_gallery_episodes_1_3.md` | 3493 | 2500 | 3 | none |
| `drafts/sample_fourfold_vampire_constraint_episodes_1_3.md` | 3596 | 2566 | 3 | none |

## 3. Deterministic Checks

Project-level:

| Command | Result |
|---|---|
| `python scripts/validate_project.py ..\projects\sample_fourfold\project.json` | `WARN`, no errors; only buffer warning |
| `python scripts/audit_narrative.py ..\projects\sample_fourfold\project.json` | `PASS` |

Draft-level:

| Draft | Lexicon Audit | Style Audit |
|---|---|---|
| `sample_fourfold_muhan_regression_episodes_1_3.md` | `PASS`, hit_count 0 | `PASS`, warnings 0 |
| `sample_fourfold_dimension_transfer_episodes_1_3.md` | `PASS`, hit_count 0 | `PASS`, warnings 0 |
| `sample_fourfold_transcendent_gallery_episodes_1_3.md` | `PASS`, hit_count 0 | `PASS`, warnings 0 |
| `sample_fourfold_vampire_constraint_episodes_1_3.md` | `PASS`, hit_count 0 | `PASS`, warnings 0 |

Manuscript guard:

- `$humanize-korean`: not actually proven. Guard reports were regenerated without `--humanized` and now mark this as `required_external_skill`.
- `ai_tell_guard.py`: not run. The manuscript guard is blocked before this step because `$humanize-korean` still needs a real pass; `tools\ai_tell_guard.py` is also unavailable in the current workspace.
- Guard report files exist under `drafts/sample_fourfold_*_guard_report.json`.

## 4. Inspection Finding And Fix

Initial per-file invariant check found one issue:

- `drafts/sample_fourfold_vampire_constraint_episodes_1_3.md` did not explicitly contain the protagonist name `이민재`.

Fix applied:

- Added an explicit self-identification line in episode 1:
  `이민재.`

Recheck result:

- all four generated draft files now include every required core invariant.

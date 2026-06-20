# Sample Fourfold Workflow Compliance Audit

Date: 2026-06-17

## Verdict

The user's concern is valid. The first drafting pass produced usable text files, but it did not fully preserve the required workflow evidence.

## Compliance Findings

| Requirement | First Pass State | Current Repair |
|---|---|---|
| Route through `webnovel-production-workflow` | Partially followed: canon, 20-episode map, narrative checks existed | Kept project plan and reran workflow validators |
| Use sample evidence as derived structure | Partially followed through `group_01_sample_calibration.json` and comparison report | Documented source limitation and per-sample functional mapping |
| Create scene/chapter contracts before drafting | Not satisfied | Added `projects/sample_fourfold/scene_contracts.json` as post-hoc repair evidence |
| Draft only from approved canon/episode plan | Mostly satisfied by `project.json`, but not proven before drafting | Existing drafts now checked against shared invariants and scene contracts |
| Run lexicon audit | Satisfied | 4 draft files PASS, hit_count 0 |
| Run style profile audit | Satisfied after fixes | 4 draft files PASS, warnings 0 |
| Apply `$humanize-korean` | Not proven | Corrected guard reports to `required_external_skill`; manuscripts are not final-complete |
| Run `ai_tell_guard.py --fail-on-s1` | Not possible | `tools/ai_tell_guard.py` is unavailable; guard remains BLOCKED |

## Corrected Status

The four draft files should be treated as workflow-repaired draft candidates, not final manuscripts.

They are valid for:

- comparing four sample-derived approaches,
- checking shared world/protagonist/story invariants,
- selecting a base version for regeneration,
- feeding a next proper loop that starts from `scene_contracts.json`.

They are not valid for:

- claiming final manuscript completion,
- claiming `$humanize-korean` was actually applied,
- claiming `ai_tell_guard.py --fail-on-s1` passed.

## Next Proper Loop

If this project is regenerated or expanded, use this order:

1. Confirm sample source state: original TXT files available or calibration-only mode.
2. Lock or update `projects/sample_fourfold/project.json`.
3. Use `projects/sample_fourfold/scene_contracts.json` as the active chapter contract.
4. Generate or revise the four drafts from those contracts.
5. Run:
   - `python scripts/validate_project.py ..\projects\sample_fourfold\project.json`
   - `python scripts/audit_narrative.py ..\projects\sample_fourfold\project.json`
   - `python scripts/audit_lexicon.py --manuscript <draft>`
   - `python scripts/audit_style_profile.py <draft> --profile templates\style_profile.json`
6. Apply `$humanize-korean` in a real pass and write a before/after summary.
7. Run `ai_tell_guard.py --fail-on-s1` if the guard becomes available.


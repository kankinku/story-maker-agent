# Independent Sample Loop Iterations 02-04 Summary

Date: 2026-06-19

## Scope

The independent per-sample loop was repeated three more times after iteration 01.

Original TXT files remain unavailable, so every same-original reference evaluation is still correctly blocked as `ORIGINAL_TXT_MISSING`. Plagiarism and copy-overlap checks remain excluded from the loop score.

## Iteration Themes

| Iteration | System Improvement Target | Output |
|---:|---|---|
| 02 | Scene-contract clarity | `agent_recreation_v2.md` for all four samples |
| 03 | Protagonist agency and pressure | `agent_recreation_v3.md` for all four samples |
| 04 | Evaluation readiness for later source-reference scoring | `agent_recreation_v4.md` for all four samples |

## Validation

| Check | Result |
|---|---|
| JSON validation for all evaluation records | PASS |
| `python scripts/audit_agent_registry.py --project-root ..` | PASS |
| `python scripts/audit_lexicon.py --manuscript <candidate>` for all v2-v4 candidates | PASS |
| `python scripts/audit_style_profile.py <candidate> --profile templates\style_profile.json` for all v2-v4 candidates | PASS after minimal channel fixes |

## Current Blocking Failure

`ORIGINAL_TXT_MISSING` remains the highest-severity blocking failure. The loop cannot honestly claim original-reference evaluation until the four TXT files are restored.

## Rerun Rule

When the source TXT files become available, rerun each sample from:

```text
element_extract -> agent_recreation -> original_reference_evaluation_without_plagiarism_check -> system_improvement -> rerun_same_sample_loop
```

Use v4 as the current best calibration-only candidate for each sample because it exposes comparable functions for later scoring.

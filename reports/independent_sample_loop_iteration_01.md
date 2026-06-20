# Independent Sample Loop Iteration 01

Date: 2026-06-19

## Mode

The loop has been started in `independent_per_sample_parallel` mode.

Each sample follows:

```text
element extraction -> agent recreation -> original-reference evaluation excluding plagiarism checks -> system improvement -> rerun same sample loop
```

## Source State

The four original TXT files are not currently present in the workspace or the searched user folders. Existing evidence proves they were processed before through `webnovel-production-agent-skill/reports/group_01_sample_calibration.json`, but that artifact does not contain the original prose.

Therefore the first loop can start only in calibration-only mode. Original-reference scoring is correctly blocked until the source TXT files are restored.

## Parallel Jobs

| Job | Element Pack | Recreation v1 | Evaluation v1 | Status |
|---|---|---|---|---|
| `sample_01_muhan_regression` | `projects/sample_independent_loops/sample_01_muhan_regression/element_pack.json` | `projects/sample_independent_loops/sample_01_muhan_regression/agent_recreation_v1.md` | `projects/sample_independent_loops/sample_01_muhan_regression/evaluation_v1.json` | BLOCKED at original-reference evaluation |
| `sample_02_dimension_transfer` | `projects/sample_independent_loops/sample_02_dimension_transfer/element_pack.json` | `projects/sample_independent_loops/sample_02_dimension_transfer/agent_recreation_v1.md` | `projects/sample_independent_loops/sample_02_dimension_transfer/evaluation_v1.json` | BLOCKED at original-reference evaluation |
| `sample_03_transcendent_gallery` | `projects/sample_independent_loops/sample_03_transcendent_gallery/element_pack.json` | `projects/sample_independent_loops/sample_03_transcendent_gallery/agent_recreation_v1.md` | `projects/sample_independent_loops/sample_03_transcendent_gallery/evaluation_v1.json` | BLOCKED at original-reference evaluation |
| `sample_04_vampire_constraint` | `projects/sample_independent_loops/sample_04_vampire_constraint/element_pack.json` | `projects/sample_independent_loops/sample_04_vampire_constraint/agent_recreation_v1.md` | `projects/sample_independent_loops/sample_04_vampire_constraint/evaluation_v1.json` | BLOCKED at original-reference evaluation |

## System Improvement Selected

Failure: `ORIGINAL_TXT_MISSING`

Responsible role: Orchestrator

Minimal fix: the loop must enforce a source availability gate before claiming original-reference evaluation. When original TXT is absent, the system may produce element packs and draft candidates from existing calibration artifacts, but the evaluation result must remain `BLOCKED`.

## Validation Results

| Check | Result |
|---|---|
| JSON validation for run manifest, element packs, and evaluation records | PASS |
| `python scripts/audit_agent_registry.py --project-root ..` | PASS |
| `python scripts/audit_lexicon.py --manuscript <candidate>` for all 4 recreations | PASS |
| `python scripts/audit_style_profile.py <candidate> --profile templates\style_profile.json` for all 4 recreations | PASS after minimal ending-open-loop fixes for sample 01 and sample 03 |

## Next Rerun Condition

Restore or attach the four original TXT files, then rerun each sample job from `element_extract`. Plagiarism and copy-overlap checks remain excluded from the loop score as requested.

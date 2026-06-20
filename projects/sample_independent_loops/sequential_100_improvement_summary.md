# Sequential 100 Improvement Loop

- Run ID: `sequential_100_improvement_loop_2026-06-19`
- Mode: one improvement per task, applied before the next task.
- Iterations recorded: `100`
- Applied rules: `100`

## First 10 Applied Improvements

- `SEQ-001` `SOURCE_AVAILABILITY_PREFLIGHT`: Original TXT availability is checked before original-reference scoring.
- `SEQ-002` `DISPLAY_NAME_UTF8_SANITY`: Sample display names must render as stable Korean labels.
- `SEQ-003` `RUN_STATUS_REFRESH`: Run manifest job statuses must reflect the latest batch result.
- `SEQ-004` `CHANNEL_CONTRACT_TEMPLATE`: Recreation candidates must declare at least two active information channels.
- `SEQ-005` `RAW_FINDING_LEDGER`: Task-level findings are stored separately from deduped system points.
- `SEQ-006` `BATCH_MODE_LABEL`: Reports distinguish structural replay from fresh creative regeneration.
- `SEQ-007` `COMPARE_GATE_FIXTURE`: Original-reference evaluation needs a fixture path even when live source TXT files are missing.
- `SEQ-008` `CANDIDATE_FINAL_GUARD_SPLIT`: Candidate artifacts and final manuscripts use different guard expectations.
- `SEQ-009` `EVALUATION_STATUS_SPLIT`: Evaluation status is split into source, style, lexicon, guard, and overall fields.
- `SEQ-010` `RAW_AND_DEDUPED_REPORTING`: Large-run reports show raw findings, deduped candidates, applied points, and pending queue.

## Artifacts

- `projects/sample_independent_loops/sequential_improvement_rules_100.json`
- `projects/sample_independent_loops/sequential_100_improvement_ledger.jsonl`
- `projects/sample_independent_loops/sequential_100_improvement_summary.json`

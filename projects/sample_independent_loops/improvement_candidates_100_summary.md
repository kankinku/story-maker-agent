# 100 Task Improvement Candidate Summary

- Source run: `sample_independent_loop_100_tasks_2026-06-19`
- Raw candidates found: `12`
- Already mapped to existing improvement points: `3`
- New queued candidates: `9`

## Existing Points

- `IP-0001`: `ORIGINAL_TXT_MISSING` - verified applied.
- `IP-0002`: `STYLE_CHANNEL_MONOTONY` - partially applied at candidate level; reusable template enforcement still needs a package-level follow-up.
- `IP-0003`: `TASK_LOCAL_RETRY_OVERHEAD` - verified applied.

## New Queued Candidates

1. `DISPLAY_NAME_ENCODING_CORRUPT`: sample metadata display names are mojibake.
2. `RUN_MANIFEST_STATUS_STALE`: run manifest job statuses still say `started_calibration_only`.
3. `TEMPLATE_ENFORCEMENT_GAP`: the channel fix was applied to candidate files, not fully enforced in the reusable template.
4. `TASK_LEDGER_TOO_COARSE`: task-level learning was hidden by deduped system points.
5. `SAME_CANDIDATE_REUSED_ACROSS_TASKS`: 100 tasks replayed v4 candidates instead of generating fresh candidates.
6. `ORIGINAL_REFERENCE_EVALUATION_UNTESTED`: compare gate remains untested because source TXT is missing.
7. `HUMANIZE_GUARD_NOT_RUN`: candidates have not entered the final manuscript guard lane.
8. `EVALUATION_STATUS_TOO_FLAT`: evaluation files hide secondary pass/fail states under one `BLOCKED` status.
9. `BATCH_SCRIPT_NOT_PACKAGE_VALIDATED`: the 100-task runner is project-local and not package-manifested.
10. `REPORT_SUMMARY_UNDERCOUNTS_FINDINGS`: final summary underreported raw findings.

## Correction

The prior answer listed only deduped/applied system points. For a 100-task learning loop, the correct reporting shape is:

`raw task findings -> deduped candidates -> selected system points -> applied changes -> next-task verification`.

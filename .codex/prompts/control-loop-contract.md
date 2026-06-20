# Control Loop Contract

Use this contract whenever Codex needs to continue through a multi-step webnovel task without asking the user for every micro-decision.

## Required Fields

```text
Goal:
Max iterations:
Check command:
Exit condition:
Iteration policy:
```

## Default Policy

1. Run the check before deciding what is fixed.
2. Treat tool output and recorded human approvals as the source of truth.
3. Pick the first highest-severity blocking failure.
4. Fix the smallest root cause that is supported by evidence.
5. Re-run the same check.
6. Report status in this shape:

```text
Iteration:
Selected failure:
Change:
Check result:
Next action:
```

## Stop Conditions

Stop immediately when:

- the exit condition is satisfied
- the max iteration count is reached
- the next change requires a human approval that has not been given
- a required tool or source artifact is unavailable
- repeated check output shows the same blocker after three repair attempts

## Webnovel Defaults

| Work Type | Max Iterations | Check |
|---|---:|---|
| Intake | 3 | minimum input checklist |
| Canon planning | 5 | canon gate checklist |
| Project validation | 8 | `validate_project.py` |
| Narrative audit | 8 | `audit_narrative.py` |
| Draft polish | 5 | `$humanize-korean` + `ai_tell_guard.py --fail-on-s1` |
| Launch package | 6 | validation + rights/IP checklist |
| Regression repair | 8 | replay + `run_regression.py` |

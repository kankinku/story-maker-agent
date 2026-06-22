# Story Maker Agent Instructions

This project is a Codex-first workspace for building and operating Korean webnovel production workflows.

## Authority Model

- `AGENTS.md` and `.codex/` contain durable Codex guidance.
- `.omx/` is runtime state only. Do not treat `.omx/` as source-of-truth instructions.
- `webnovel-production-agent-skill/` is the source package for the Web Novel Production Loop.
- For Korean manuscript generation or rewrite, the post-draft order is mandatory:
  `draft -> source-fidelity audit when source-based -> $humanize-korean -> ai_tell_guard.py --fail-on-s1` when the guard is available in the active story workspace.

## Routing Rule

When a user request is about webnovel planning, episodes, serialization, platform packaging, story bible, character/world continuity, reader metrics, comments, failure diagnosis, revision, or manuscript drafting, use the project workflow skill:

`.codex/skills/webnovel-production-workflow/SKILL.md`

Do not jump directly to long manuscript drafting unless the workflow gates allow it.

## Source Remake Isolation Rule

For a sample/source remake, use `source lock -> extract world/character/protagonist/ability/story-engine -> abstract -> human-approved remake blueprint -> new Story Bible and episode plan -> draft -> isolated source comparison`.

- Do not put the original manuscript, long excerpts, dialogue lists, or sequential source-scene summaries in the Writer prompt.
- The Writer may consume only the approved remake blueprint, derived Story Bible, new episode plan, episode contract, and current state.
- Reopen the original only after drafting for setting-fidelity and surface-copy comparison.
- If raw source content reaches Writer Context, stop with `RAW_SOURCE_IN_WRITER_CONTEXT`.

## Workflow Gates

Use this order unless the user explicitly asks for a narrower task:

1. Intake: classify intent, collect minimum inputs, identify missing decisions.
2. Market evidence: refresh platform facts when recommending a real platform or publishing move.
3. Canon lock: establish concept, promise, ending direction, story bible version, and change policy.
4. Serial plan: build or update the 20-episode map.
5. Narrative audit: check opening contract, protagonist advantage, POV/exposition, foreshadow ledger, phase map, and scale ladder.
6. Draft buffer: expand approved episode plans into scenes and drafts.
7. Polish and guard: run Korean humanization and AI-tell guard for manuscript outputs.
8. Launch package: prepare title, blurbs, tags, age rating, notice, schedule, and buffer.
9. Observe: review metrics/comments on a fixed cadence without immediate canon churn.
10. Repair: trace, diagnose, propose patch, wait for human approval, replay, run regression, then lock.

## Control Loop Policy

Current system version is `webnovel-production-loop@1.17.0`. Previously collected sample ledgers, evaluations, candidates, and rule packs are historical evidence governed by `projects/sample_independent_loops/context_compounding_migration.json`; they are not current policy or canon. Current prompt/policy/data alignment must pass `python webnovel-production-agent-skill/scripts/audit_current_system_alignment.py --project-root .` after workflow changes.

Treat non-trivial webnovel work as a finite state machine, not a one-shot prompt.

Each loop must define:

- `Goal`: the semantic target for this phase.
- `Exit when`: observable conditions that prove the phase is done.
- `Max iterations`: the retry budget before stopping.
- `Check command`: deterministic checks or human approval required between iterations.
- `Iteration policy`: run checks, pick the highest-severity first failure, apply the smallest responsible change, re-run checks, then report status.

Default iteration budgets:

- Intake and missing-input resolution: 3
- Canon and planning repair: 5
- Narrative validation repair: 8
- Draft and rewrite polish: 5
- Launch package repair: 6
- Incident replay and regression: 8

Stop early when exit conditions pass. If the max iteration count is reached, stop and report the remaining failure codes, attempted fixes, and the next human decision needed.

Do not make broad speculative rewrites to clear multiple failures at once. Fix the first highest-severity root cause that is supported by the check output.

## Required Local Checks

On Windows PowerShell, set `$env:PYTHONUTF8=1` for Python checks and use `Get-Content -Encoding UTF8` when inspecting Korean JSON or manuscript files. Do not treat default-encoding mojibake as source corruption.

From `webnovel-production-agent-skill/`, use these commands when the relevant artifact exists:

```powershell
python scripts/validate_project.py <project.json>
python scripts/audit_narrative.py <project.json>
python scripts/run_regression.py tests/regression_cases.json
```

For package changes, also run:

```powershell
python scripts/build_export.py --output dist/webnovel-production-loop.skill.json
python scripts/run_portable_export_tests.py
python scripts/audit_workspace_projects.py --project-root ..
```

## Completion Rule

For workflow or package changes, report changed files and verification results.

For manuscript work, do not mark complete until humanization and the AI-tell gate are complete, or until the missing guard/tool is explicitly reported as unavailable.

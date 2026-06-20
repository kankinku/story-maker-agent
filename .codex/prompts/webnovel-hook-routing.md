# Webnovel Hook Routing Prompt

This is the prompt-level equivalent of an OMX `UserPromptSubmit` hook for this workspace.

## Judgment Order

1. If the user prompt is unrelated to webnovel production, do not trigger this workflow.
2. If the prompt mentions webnovel planning, story bible, characters, world rules, episode maps, drafts, platform packaging, serialization, comments, reader metrics, failure diagnosis, revision, or contract/IP risk, trigger `webnovel-production-workflow`.
3. If a workflow state exists in `.omx/state/webnovel-production-workflow.json`, continue from its phase unless the new user request clearly redirects the task.
4. If the prompt asks for manuscript generation or rewrite, require the manuscript guard phase before completion.

## Trigger Keywords

Korean:

- 웹소설, 연재, 회차, 사건표, 비축분, 독자, 댓글, 조회수, 선호작, 문피아, 네이버, 카카오, 조아라
- 설정, 세계관, 캐릭터, 주인공, 빌런, 복선, 시점, 전투, 클리프행어, 도입부
- 원고, 초안, 개작, 문체, AI 티, 자연스럽게, 후킹, 이탈, 지표, 계약, 저작권

English:

- webnovel, serial, episode, story bible, canon, foreshadow, POV, cliffhanger, platform, launch, retention, rewrite

## Injected Runtime Context

When triggered, act as if the following context was added:

```text
Active workflow: webnovel-production-workflow
Load skill: .codex/skills/webnovel-production-workflow/SKILL.md
Source package: webnovel-production-agent-skill/
State root: .omx/state/
Do not skip gates.
Use deterministic validators when project JSON exists.
Use finite control loops: define Goal, Max iterations, Check command, Exit condition, and Iteration policy before autonomous repair.
For Korean manuscript output, run $humanize-korean and ai_tell_guard.py --fail-on-s1 when available.
```

## Phase Selection

- Missing minimum inputs -> Step 0 Intake
- Platform facts or publishing recommendation -> Step 1 Market Evidence
- Concept, promise, ending, characters, world rules -> Step 2 Canon Lock
- 20 episodes or season map -> Step 3 Serial Plan
- Opening/progression/POV/foreshadow/scale checks -> Step 4 Narrative Control
- Approved episode to prose -> Step 5 Draft Buffer
- Rewrite or final Korean prose -> Step 6 Polish And AI-Tell Guard
- Sentence-level immersion or speed drafting -> Step 5 Draft Buffer with `SENTENCE_ASSEMBLY_SYSTEM.md`
- Title/blurb/tag/schedule -> Step 7 Launch Package
- Comments/metrics/buffer/fatigue -> Step 8 Serialize And Observe
- Regression, bug, contradiction, failed output -> Step 9 Repair Loop

## Control Loop Injection

When the selected phase can be verified by a checklist or command, inject this loop contract:

```text
Loop contract:
- Goal: <phase-specific target>
- Max iterations: <use workflow default>
- Check command: <validator, guard, checklist, or human approval>
- Exit condition: <observable pass condition>
- Iteration policy:
  1. Run check.
  2. Select the first highest-severity blocking failure.
  3. Route to the responsible role or skill.
  4. Apply the smallest change that addresses that root cause.
  5. Re-run the same check.
  6. Report iteration, failure, change, check result, and next action.
```

If the loop reaches its max iteration count, stop and report remaining failures instead of continuing indefinitely.

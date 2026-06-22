# Webnovel Production Workflow

Use this skill when the user asks Codex to plan, draft, revise, serialize, package, operate, or diagnose a webnovel project.

This workflow adapts the `oh-my-codex` pattern to this workspace:

- `.codex/` contains durable Codex instructions, skills, agents, and prompt routing.
- `.omx/` may hold runtime state, logs, plans, and handoff context, but it is not the instruction source.
- `webnovel-production-agent-skill/` contains the underlying production-loop package and validators.

## Hook Judgment

Classify every user prompt before acting.

| Intent | Trigger Examples | Route | First Action |
|---|---|---|---|
| `quick_answer` | "이 설정 어때?", "짧게 평가" | Direct answer | Answer without creating artifacts unless needed. |
| `ideation` | 아이디어, 소재, 장르 후보, 콘셉트 | Step 0 | Ask only for missing minimum inputs or produce bounded hypotheses. |
| `planning` | 세계관, 캐릭터, Story Bible, 20화 사건표 | Steps 2-4 | Build canon and serial plan before drafting. |
| `drafting` | 1화 써줘, 회차 원고, 장면 확장 | Steps 4-6 | Verify approved episode plan before draft. |
| `rewrite` | 고쳐줘, 자연스럽게, AI 티 제거 | Step 6 | Preserve facts, use sentence assembly, then run `$humanize-korean` and AI-tell guard. |
| `platform` | 네이버, 문피아, 카카오, 조아라, 제목/소개/태그 | Steps 1, 7 | Refresh platform evidence before recommendation. |
| `ops` | 댓글, 조회수, 지표, 이탈, 연재 주기 | Step 8 | Separate signal, sample size, schedule, buffer, and canon impact. |
| `incident` | 실패, 설정 충돌, 독자 반응 악화, 회귀 테스트 | Step 9 | Trace -> diagnose -> patch proposal -> approval -> replay -> regression. |
| `rights` | 계약, 저작권, 팬픽, 2차 사업 | Step 7 rights gate | Provide checklist and escalate legal conclusions. |

If the prompt matches multiple intents, choose the earliest required gate. Example: "1화 써줘" with no canon starts at intake/canon, not drafting.

Use `python scripts/route_intent.py <intent>` as the deterministic route contract before selecting a phase or specialist role.

## Minimum Inputs

Do not proceed past Step 0 without either confirmed inputs or clearly labeled assumptions for:

- genre or genre candidates
- one-line concept or idea note
- primary goal: completion practice, test serialization, contest, monetization, or other
- sustainable weekly writing time

For planning beyond concept, also capture:

- target reader and emotional reward
- target platform candidates
- forbidden material and IP risks
- ending direction
- reference works and which aspects may be referenced

## Control Loop Specification

This workflow is a finite control loop. Do not treat it as a single prompt that should produce a final answer in one pass.

### Loop State

Track the following state mentally, and in `.omx/state/webnovel-production-workflow.json` when runtime state is being maintained:

- `phase`
- `goal`
- `exit_when`
- `iteration`
- `max_iterations`
- `check_commands`
- `last_check_result`
- `selected_failure`
- `selected_agent`
- `next_action`
- `blocked_reason`

### Default Loop Budgets

| Loop | Max Iterations | Primary Check | Exit When |
|---|---:|---|---|
| `intake_loop` | 3 | Minimum input checklist | Required inputs are confirmed or assumptions are labeled. |
| `canon_loop` | 5 | Canon gate review | Concept, promise, ending direction, story bible version, and change policy exist. |
| `serial_plan_loop` | 5 | `validate_project.py` when project JSON exists | 20 episodes, opening hooks/conflicts, and episode endings pass. |
| `narrative_control_loop` | 8 | `validate_project.py` + `audit_narrative.py` | Both checks return `PASS`, or remaining issues are explicit human decisions. |
| `engagement_contract_loop` | 5 | `audit_engagement_contract.py` + semantic rubric | Character-first episode contract passes and all engagement dimensions have scene evidence. |
| `lexicon_control_loop` | 5 | `audit_lexicon.py` + sample calibration report when samples exist | Lexicon files pass; manuscript has no unjustified S1 AI-tell/prohibited phrase hits. |
| `sample_style_loop` | 5 | `calibrate_from_samples.py` + `audit_style_profile.py` + rubric review | Sample-derived style rules are reviewed, applied through scene contracts, and warnings are resolved or justified. |
| `context_compounding_loop` | 5 | `audit_context_compounding.py` | Required evidence and state pass; review and promotion artifacts obey approval gates. |
| `draft_polish_loop` | 5 | Humanization + AI-tell guard when available | Draft preserves canon and S1 gate passes or exceptions are justified. |
| `launch_loop` | 6 | `validate_project.py` + rights/IP checklist | Launch metadata, buffer, IP, and approval gates pass. |
| `repair_loop` | 8 | Original replay + regression suite | Original failure passes and critical regressions pass. |

### Iteration Policy

Each iteration must follow this order:

1. Run the relevant check command or checklist.
2. Read the observed result before proposing a fix.
3. Select the first highest-severity failure that blocks the exit condition.
4. Map that failure to one responsible role or skill.
5. Apply the smallest change that addresses that root cause.
6. Re-run the same check.
7. Report: iteration number, selected failure, change made, check result, next action.

Do not:

- fix unrelated failures in the same iteration unless they share the same root cause
- rewrite the entire plan to hide a narrow schema or audit failure
- advance to manuscript drafting while canon, serial plan, or narrative control gates are failing
- call a phase complete based only on model judgment when a check command exists

### Check Commands

When a `project.json` artifact exists under the active project, run from `webnovel-production-agent-skill/`:

```powershell
python scripts/validate_project.py <project.json>
python scripts/audit_narrative.py <project.json>
```

When lexicons or Korean manuscript vocabulary/style rules change, run:

```powershell
python scripts/audit_lexicon.py
python scripts/audit_lexicon.py --manuscript <draft-path>
python scripts/calibrate_from_samples.py <sample-dir> --output <report.json> --path-mode basename
python scripts/audit_style_profile.py <draft-path> --profile templates/style_profile.json
python scripts/run_semantic_rubric.py <chapter-audit.json> --include-style
```

Before non-trivial episode drafting, run:

```powershell
python scripts/audit_engagement_contract.py <scene-contract.json> --story-bible <story-bible.json>
```

Use `ENGAGEMENT_CHARACTER_SYSTEM.md` for character-first canon, the ten evidence-backed engagement dimensions, and the separate readability delivery gate.

When the project is a dimension-transfer survival expedition, read these references before planning or drafting:

```text
references/dimension-survival/survival-expedition-loop.md
references/dimension-survival/resource-choice-and-conversion.md
references/dimension-survival/procedural-exposition.md
references/dimension-survival/utility-to-trust-relationship.md
references/styles/dimension-survival-expedition.md
```

When the project is a transcendent-gallery mentored tower climb, read these references before planning or drafting:

```text
references/transcendent-gallery/distributed-mentor-feedback.md
references/transcendent-gallery/evidence-based-combat-review.md
references/transcendent-gallery/one-life-tower-progression.md
references/transcendent-gallery/gallery-emotional-chorus.md
references/styles/transcendent-gallery-climb.md
```

When the project is a vampire-retainer misunderstanding comedy, read these references before planning or drafting:

```text
references/vampire-retainer/evidence-based-misunderstanding.md
references/vampire-retainer/delegated-combat-and-agency.md
references/vampire-retainer/retainer-growth-economy.md
references/vampire-retainer/supernatural-domestic-comedy.md
references/styles/vampire-retainer-misunderstanding.md
```

When the package, validators, fixtures, or workflow rules change, run:

```powershell
python scripts/audit_lexicon.py
python scripts/run_regression.py tests/regression_cases.json
python scripts/build_export.py --output dist/webnovel-production-loop.skill.json
python scripts/run_portable_export_tests.py
python scripts/audit_workspace_projects.py --project-root ..
```

For context-compounded drafting and review, run:

```powershell
python scripts/audit_context_compounding.py inner <context-plan.json> <evidence-pack.json>
python scripts/audit_context_compounding.py state <character-state.json> <relationship-state.json> <roleplay-result.json> <episode-memory-delta.json>
python scripts/audit_context_compounding.py review <review-packet.json>
python scripts/audit_context_compounding.py control <change-proposal.json> <component-version-registry.json>
python scripts/evaluate_change_replay.py <replay-evaluation.json> --proposal <change-proposal.json> --apply
python scripts/run_context_compounding_tests.py
python scripts/migrate_legacy_context_data.py --project-root ..
python scripts/audit_current_system_alignment.py --project-root ..
```

For Korean manuscript generation or rewrite, run the manuscript guard in the active story workspace:

```text
$humanize-korean
python .\tools\ai_tell_guard.py <draft-path> --output <report-path> --fail-on-s1
```

Record `$humanize-korean` completion as JSON containing `status: PASS`, `skill: humanize-korean`, the absolute manuscript path, and the SHA-256 of the exact guarded manuscript. `--humanized` without this hash-bound report does not satisfy completion.

## Workflow Phases

### Step 0 - Intake

Role: Orchestrator

Loop: `intake_loop`

Goal:

- Convert the user's request into a phase, required inputs, and observable exit conditions.

Exit when:

- intent is classified
- minimum inputs are confirmed or assumptions are labeled
- next phase is selected

Outputs:

- intent classification
- missing input list
- assumptions, if any
- initial project state

Gate G0:

- genre hypothesis, target reader, story promise, and weekly availability are known or explicitly assumed.

### Step 1 - Market Evidence

Role: Market Researcher

Loop: `canon_loop` when platform facts influence canon, otherwise `launch_loop`

Goal:

- Separate current official facts from observations and inferences before recommending platform-specific actions.

Exit when:

- sources are current enough for the recommendation
- stale or missing facts are explicitly labeled

Use when the task recommends a real platform, title/tag packaging, launch timing, contest path, ranking assumptions, or monetization route.

Rules:

- Refresh official sources when facts may have changed.
- Separate official fact, observation, and inference.
- Mark platform profile stale when older than 30 days.

Output:

- platform evidence table
- practical hypotheses with confidence
- missing or unverifiable facts

### Step 2 - Canon Lock

Role: Story Architect

Loop: `canon_loop`

Goal:

- Lock the minimum viable canon needed for serial planning.

Exit when:

- concept, promise, ending direction, story bible version, and explicit approval policy exist

Outputs:

- one-line concept
- logline: protagonist, current lack/situation, self-chosen goal, unique means/constraint, ending direction
- story promise
- ending direction
- character-first sheets: desire, stakes, principle, contradiction/flaw, choice and speech signatures, relationship variation, repeatable appeal, change direction
- world rules
- `story_bible_version`
- canon change policy: `explicit_approval`

Gate G1:

- Do not build a 20-episode plan if ending direction or story promise is empty.
- Canon-changing ideas become change requests, not silent edits.

### Step 3 - Serial Plan

Role: Story Architect

Loop: `serial_plan_loop`

Goal:

- Produce a validator-ready serial plan.

Exit when:

- the plan has at least 20 episodes
- episodes 1-3 have hooks and conflicts
- every planned episode has a cliffhanger or next reason

Outputs:

- 20-episode map
- hooks and conflicts for episodes 1-3
- cliffhanger or next reason for every planned episode
- buffer target and cadence

Gate G2:

- 20 planned episodes exist.
- Episodes 1-3 have hook and conflict.
- Every episode has cliffhanger or next reason.

### Step 4 - Narrative Control

Roles:

- Narrative Engagement Editor
- Progression & Foreshadowing Editor
- Continuity Editor

Loop: `narrative_control_loop`

Goal:

- Make the project pass deterministic narrative control gates.

Exit when:

- `validate_project.py` returns `PASS`
- `audit_narrative.py` returns `PASS`
- any remaining issue is a recorded human decision rather than an unhandled defect

Required structures:

- Opening Contract
- Protagonist Advantage Map
- POV and Exposition Policy
- Foreshadow Ledger
- Phase Map
- Scale Ladder
- relationship anchors for stage transitions
- character-first canon and engagement evidence map

Run:

```powershell
python scripts/validate_project.py <project.json>
python scripts/audit_narrative.py <project.json>
```

Gate:

- Both checks must be `PASS` or failures must be turned into explicit patch proposals.

### Step 5 - Draft Buffer

Role: Episode Writer

Loop: `draft_polish_loop`

Goal:

- Convert approved episode plans into manuscript drafts without changing canon silently.
- Use the sentence assembly system: internal monologue, sensory dynamic description, and curiosity injection.
- When sample style is requested, use `style profile -> scene contract -> draft -> style audit`, not a one-shot style prompt.

Exit when:

- draft follows approved canon and episode plan
- sentence blocks have clear functions rather than flat action listing
- sample-derived channel/rhythm/reversal rules are either satisfied or exceptions are recorded
- change requests are separated from prose
- manuscript guard phase is complete for Korean final prose

Rules:

- Create a Context Plan and passing Evidence Pack before non-trivial drafting.
- Load structured character and relationship state, then produce structured roleplay as input only.
- Generate at most two Writer candidates; select one and never merge candidate paragraphs automatically.
- Draft only from approved canon and episode plan.
- Keep scene goal, obstacle, choice, and consequence visible.
- Before drafting from a sample style profile, create a chapter contract with state change, core expectation, core reversal, reader reward, ending open loop, and active information channels.
- For every non-trivial draft, create a character-first engagement contract with primary desire, protagonist-initiated choice, resolved question, concrete state change, earned reward, relationship delta, intended relief function, and a specific next-episode question.
- Every scene must advance at least one of plot, character, relationship, or a world rule in use. New exposition must have a scene trigger and immediate use.
- Audit the scene contract with `audit_engagement_contract.py` before drafting.
- Use sample evidence only as derived structure: information channels, paragraph rhythm, micro-beats, retry loop, and anti-patterns. Do not copy sample phrases, jokes, names, or event order.
- For dimension-transfer survival expeditions, drive episodes through deficit, timed expedition, resource choice, return conversion, base improvement, and the next bottleneck.
- Track named dimensions, inventory, equipment dependencies, abandoned resources, unresolved threats, and revisit availability when they appear.
- For transcendent-gallery tower climbs, preserve plural imperfect mentor advice, protagonist selection/modification, one-life preparation, uploaded evidence, and post-combat review lessons.
- For vampire-retainer misunderstanding comedy, preserve evidence-based misunderstanding, delegated combat with protagonist strategy, retainer differentiation, blood-resource economy, and outside perspectives that trigger new events.
- Assemble prose as `internal monologue -> sensory dynamic description -> curiosity injection` when a scene needs immersion.
- Prefer concrete dynamic verbs over flat action labels.
- Keep hidden information fair: withhold enough to create curiosity, not enough to break causality.
- Do not add core setting facts outside the Story Bible.
- If canon must change, output a change request.
- After human approval, propose an Episode Memory Delta. Commit only after Continuity PASS and explicit approval ID.

Outputs:

- scene list
- draft
- edit notes
- canon-change requests, if any

### Step 6 - Polish And AI-Tell Guard

Use for Korean manuscript output.

Loop: `draft_polish_loop`

Goal:

- Remove avoidable AI-tell/style issues without changing facts or story structure.

Exit when:

- source-based rewrites pass a hash-bound rewrite fidelity contract
- `$humanize-korean` has been applied
- a hash-bound humanization report matches the exact manuscript
- `ai_tell_guard.py --fail-on-s1` passes, or remaining S1 findings are explicitly justified

Required order:

1. For source-based rewrites, build `templates/rewrite_fidelity_contract.json` from the source/rewrite pair and run `python scripts/audit_rewrite_fidelity.py <contract.json>` before style polishing.
2. Run `python scripts/audit_lexicon.py --manuscript <draft-path>` from `webnovel-production-agent-skill/` when the draft is available as a file.
3. If a sample style profile was used, run `python scripts/audit_style_profile.py <draft-path> --profile <style-profile.json>` and resolve or justify warnings.
4. If semantic scores are available, run `python scripts/run_semantic_rubric.py <chapter-audit.json> --include-style`.
5. Apply `$humanize-korean` to the full draft while preserving facts, names, event order, viewpoint, dialogue speakers, numbers, and direct quotes.
6. Save the absolute manuscript path and SHA-256 in the humanization report.
7. Run `ai_tell_guard.py --fail-on-s1` when the active story workspace provides the guard.
8. If S1 findings remain, justify each as dialogue, direct quote, status UI, or false positive before completion.

Gate:

- Do not claim manuscript completion before this phase is done or explicitly blocked by missing tooling.

### Step 7 - Launch Package

Roles:

- Market Researcher
- Serial Operations Analyst
- Rights & Contract Reviewer when relevant

Loop: `launch_loop`

Goal:

- Build a launch-ready package whose metadata, buffer, platform facts, and risk gates are observable.

Exit when:

- launch metadata is complete
- buffer gate passes
- IP review is cleared
- writer approval is recorded

Outputs:

- title candidates
- short and long blurbs
- tags
- age rating
- author notice
- launch schedule
- buffer status
- IP review status

Gate G3:

- validation errors: 0
- high-risk warnings: resolved or human-approved
- IP status cleared for launch
- writer approval received

### Step 8 - Serialize And Observe

Role: Serial Operations Analyst

Loop: weekly observation loop

Goal:

- Convert metrics and comments into bounded hypotheses without causing reaction-driven canon churn.

Exit when:

- signals are categorized
- sample-size uncertainty is stated
- decision is one of maintain, modify, discard, or keep observing

Track:

- post time and platform
- episode version
- views, favorites, comments, sales/support signals if available
- comment categories: praise, confusion, criticism, request, abuse
- buffer change
- author fatigue

Rules:

- Do not rewrite canon from a small comment sample.
- Use fixed review cadence.
- Distinguish discovery failure, promise failure, payoff failure, schedule failure, genre mismatch, and sample-size uncertainty.

### Step 9 - Repair Loop

Roles:

- Incident Diagnoser
- relevant specialist role for patch
- Orchestrator for approval and promotion

Loop: `repair_loop`

Goal:

- Fix the smallest verified root cause of a failed output or workflow run and prevent recurrence.

Exit when:

- original failing input replays successfully
- critical regressions pass
- new regression case is saved when applicable
- version promotion or blocked status is recorded

Process:

1. Build trace bundle.
2. Produce at least three cause hypotheses.
3. Select minimum responsible scope.
4. Propose patch and expected effect.
5. Wait for human approval.
6. Replay original failing input.
7. Run deterministic validation and regression.
8. Save a regression case.
9. Promote project or story bible version.

For human-edit system improvement, require a distinct draft/final Review Packet. Classify the Review Diff, generate at least three cause hypotheses, and inspect only the latest ten completed reviews. A Change Proposal requires three occurrences of the same classification and scope. Candidate creation, one-task canary, and final promotion each remain human-controlled; any replay or canary regression rolls back.

Run when package artifacts change:

```powershell
python scripts/run_regression.py tests/regression_cases.json
python scripts/build_export.py --output dist/webnovel-production-loop.skill.json
```

## Failure Code To Action Map

| Failure | Responsible Role | Minimal Action |
|---|---|---|
| `SCHEMA` | Orchestrator | Fix JSON shape first; do not infer quality. |
| `ENDING_MISSING` | Story Architect | Ask for or propose 2-3 ending directions. |
| `EPISODE_PLAN_SHORT` | Story Architect | Build to at least 20 episodes before drafting. |
| `OPENING_HOOK_MISSING` | Narrative Engagement Editor | Rewrite episodes 1-3 around immediate curiosity. |
| `OPENING_COMBAT_ANCHOR` | Narrative Engagement Editor | Define why combat reveals character, stakes, cost, or hidden card. |
| `ADVANTAGE_MISSING` | Progression & Foreshadowing Editor | Fill profession, ability synergy, unique domain, boundary, and cost. |
| `ADVANTAGE_PROOF_NOT_PLANNED` | Progression & Foreshadowing Editor | Add proof scenes in the stated proof episodes. |
| `POV_POLICY_MISSING` | Continuity Editor | Define primary POV, allowed variants, and switch markers. |
| `EXPOSITION_BUDGET_EXCEEDED` | Continuity Editor | Move terms later or convert explanation into scene action. |
| `FORESHADOW_REMINDER_MISSING` | Progression & Foreshadowing Editor | Add reminder beat before payoff when gap exceeds 8 episodes. |
| `PHASE_MAP_INCOMPLETE` | Progression & Foreshadowing Editor | Add imprint, growth, relationship, and scale phases. |
| `SCALE_LADDER_INCOMPLETE` | Progression & Foreshadowing Editor | Define escalation that changes problem type, not only size. |
| `REACTION_SCHEDULE_MISSING` | Serial Operations Analyst | Set review cadence before using reader response. |
| `IP_REVIEW_NOT_CLEARED` | Rights & Contract Reviewer | Stop launch and produce risk checklist. |
| `CONTEXT_REQUIRED_MISSING` | Context & Evidence Planner | Retrieve or resolve the required context before drafting. |
| `EVIDENCE_CONFLICT_UNRESOLVED` | Context & Evidence Planner | Block drafting and request canonical resolution. |
| `STALE_CONTEXT` | Context & Evidence Planner | Refresh the structured source. |
| `CHARACTER_STATE_DRIFT` | Character State Keeper | Align scene or delta with the current snapshot. |
| `CANON_DELTA_UNAPPROVED` | Character State Keeper | Do not commit without Continuity PASS and approval ID. |
| `REVIEW_PAIR_MISSING` | Review Diff Analyst | Require distinct draft and approved-final files. |
| `PROMOTION_APPROVAL_MISSING` | Orchestrator | Keep the component inactive. |
| `REGRESSION_DETECTED` | Incident Diagnoser | Block promotion and roll back. |
| `CANON_TARGET_UNSUPPORTED` | Story Architect | Route canon facts through a separately approved Story Bible change. |
| `REPLAY_ARTIFACT_MISSING` | Incident Diagnoser | Require real current, candidate, and human-final files. |
| `STATE_ID_DUPLICATE` | Character State Keeper | Deduplicate state and roleplay identifiers. |
| `CHARACTER_KNOWLEDGE_LEAK` | Character State Keeper | Restore the character knowledge boundary or add canonical learning evidence. |
| `EVIDENCE_ID_DUPLICATE` | Context & Evidence Planner | Resolve duplicate context IDs before drafting. |
| `ROLLBACK_REASON_MISSING` | Orchestrator | Require replay or canary regression evidence. |
| `HUMANIZATION_EVIDENCE_MISSING` | Episode Writer | Attach a path-and-hash-bound humanization report. |
| `ENGAGEMENT_EPISODE_FIELD_MISSING` | Story Architect | Fill the missing character-choice, payoff, state-change, or next-question field before drafting. |
| `ENGAGEMENT_CHARACTER_FIELD_MISSING` | Story Architect | Complete the character-first canon before planning scenes. |
| `ENGAGEMENT_LOGLINE_FIELD_MISSING` | Story Architect | Complete the character-first logline before serial planning. |
| `ENGAGEMENT_SCENE_NO_ADVANCE` | Episode Writer | Remove, compress, or revise the scene so it advances plot, character, relationship, or a world rule in use. |
| `RUBRIC_EVIDENCE_MISSING` | Narrative Engagement Editor | Attach a concrete scene or artifact reference to every semantic score. |
| `INVALID_STATE_TRANSITION` | Orchestrator | Start a new run instead of mutating a terminal run. |

## State Handoff

If maintaining runtime state, use `.omx/state/webnovel-production-workflow.json` with this shape:

```json
{
  "active": true,
  "workflow": "webnovel-production-workflow",
  "phase": "intake",
  "project_id": "",
  "project_version": "",
  "story_bible_version": "",
  "last_gate": "G0",
  "goal": "",
  "exit_when": [],
  "iteration": 0,
  "max_iterations": 0,
  "check_commands": [],
  "last_check_result": "",
  "selected_failure": "",
  "selected_agent": "",
  "next_action": "",
  "blocked_reason": "",
  "updated_at": ""
}
```

Treat this as resumable status only. Source documents and Codex instructions remain in tracked project files.

## Completion Checklist

- State the phase completed.
- State the loop name and iteration count when a loop was used.
- List artifacts changed or produced.
- Report validation commands and results.
- Report the selected failure and minimal fix when a repair iteration happened.
- For drafting, report how sentence assembly was applied or why it was not relevant.
- For manuscripts, report humanization and AI-tell guard result.
- If blocked, state the exact missing input, missing tool, or failed gate.

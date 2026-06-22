# Changelog

## 1.15.0

- Added a character-first canon contract covering desire, stakes, principle, contradiction, choice/speech signatures, relationship variation, repeatable appeal, and ending change.
- Converted abstract fun/dopamine guidance into ten evidence-backed engagement dimensions plus a separate readability delivery gate.
- Expanded scene and chapter contracts with protagonist-initiated choice, resolved question, concrete state change, earned payoff, relationship delta, scene advances, exposition trigger/use, and a specific next-episode question.
- Added a deterministic engagement-contract auditor, pass/fail fixtures, regression runner, prompt routing, failure codes, and synchronized package documentation.
- Embedded every runtime config, schema, template, prompt, lexicon, source, and reference asset in the single-JSON export and added isolated rehydration tests.
- Added cross-surface 1.15.0 alignment checks for Codex routing, component registry, review packets, and current fixtures.
- Made character-first logline/canon fields part of the main project schema and validator, and required per-dimension evidence for semantic scores.
- Added explicit workspace project classification so current projects validate while historical under-length chunks remain evidence-only blocked content.

## 1.14.0

- Added deterministic routing for all nine intents and synchronized workflow step numbers.
- Blocked silent canon-delta drops, duplicate evidence/state/review IDs, unauthorized secret knowledge, and ungrounded rollback.
- Required real Review/Replay artifacts, hash-bound humanization evidence, resumable control-loop state, and top-level Context evidence contracts.
- Added schema validation, UTF-8 BOM compatibility, explicit legacy source-availability semantics, and expanded regression suites.

## 1.13.0

- Migrated all collected sample-loop data through a non-destructive context-compounding provenance index with hashes, authority, current use, and candidate resolutions.
- Marked historical ledgers, evaluations, candidates, summaries, and rule packs as episodic or derived evidence rather than active policy or canon.
- Added the shared Context-Compounding Contract to all 13 role prompts.
- Connected sample evaluation, source chunks, project templates, evaluation policy, and improvement points to Context Plan, Evidence Pack, state, review, replay, canary, approval, and rollback gates.
- Made legacy project runners read-only by default so historical task-local rule application cannot overwrite the current system.
- Added current-system alignment audit covering prompts, policies, templates, data hashes, candidate resolutions, and platform-profile freshness.

## 1.12.0

- Added Context Plan, Evidence Pack, character/relationship state, structured roleplay, approved episode delta, Review Packet/Diff, Change Proposal, and component version contracts.
- Added Context & Evidence Planner, Character State Keeper, and Review Diff Analyst while preserving one canonical Orchestrator.
- Added deterministic Inner, state, review, replay, canary, promotion, and rollback gates.
- Added multi-dimensional Offline Replay evaluation for result quality, canon fidelity, state continuity, process compliance, style fit, and efficiency.
- Added explicit manuscript diff aggregation: latest ten completed reviews, three same-scope occurrences, and no more than three proposals.
- Kept all component promotion human-approved; no Vector DB, external publish, durable queue, or automatic rule promotion was added.

## 1.11.0

- `references/transcendent-gallery/` added for transcendent-gallery tower-climb samples:
  - `distributed-mentor-feedback.md`
  - `evidence-based-combat-review.md`
  - `one-life-tower-progression.md`
  - `gallery-emotional-chorus.md`
- `references/styles/transcendent-gallery-climb.md` added.
- `references/vampire-retainer/` added for vampire-retainer misunderstanding comedy samples:
  - `evidence-based-misunderstanding.md`
  - `delegated-combat-and-agency.md`
  - `retainer-growth-economy.md`
  - `supernatural-domestic-comedy.md`
- `references/styles/vampire-retainer-misunderstanding.md` added.
- `templates/mentor_knowledge_state.json`, `stage_history.json`, `retainer_registry.json`, `reputation_belief_state.json`, `hidden_identity_state.json` added.
- Episode Writer, Narrative Engagement Editor, Continuity Editor, and the local Codex workflow now route, draft, audit, and track continuity for both engines.

## 1.10.0

- `references/dimension-survival/` 추가: 제한시간형 차원 원정과 파밍 기반 생존 성장 샘플 분석을 네 모듈로 분리.
  - `survival-expedition-loop.md`
  - `resource-choice-and-conversion.md`
  - `procedural-exposition.md`
  - `utility-to-trust-relationship.md`
- `references/styles/dimension-survival-expedition.md` 추가: 1인칭 실용 생존자 시점, 절차적 설명, 전술 행동, 귀환 보상 리듬을 스타일 모듈로 정리.
- `templates/dimension_contract.json`, `inventory_state.json`, `equipment_dependency.json` 추가.
- Episode Writer, Narrative Engagement Editor, Continuity Editor에 결핍, 시간 압력, 적재 제한, 자원 선택, 귀환 재가공, 장비 의존성, 조력자 만능화 방지 규칙 반영.
- 로컬 Codex workflow에 차원이동 생존 원정 reference 라우팅과 상태 추적 규칙 추가.

## 1.9.0

- `SAMPLE_STYLE_PROTOCOL.md` 추가: 샘플 문체를 원문 모사가 아니라 정보 채널, 문단 리듬, 마이크로 비트, 도전 루프, 기대-반전-보상 구조로 이식하는 절차 정의.
- `templates/style_profile.json`, `scene_contract.json`, `chapter_audit.json` 추가.
- `scripts/audit_style_profile.py` 추가: 원고의 문단 길이, 짧은 줄 비율, 장문 연속, 정보 채널 다양성, 화말 열린 고리 감사.
- `scripts/run_semantic_rubric.py` 추가: 사람 또는 judge가 작성한 1~5 의미 루브릭 점수를 정책 기준으로 검증.
- `calibrate_from_samples.py`가 샘플의 line-structure 후보를 함께 산출하도록 확장.
- Episode Writer와 Narrative Engagement Editor에 샘플 구조 이식 규칙과 회차 계약/장면 비트 절차 반영.
- `generate_test_report.py`, manifest, metadata, export 번들에 새 검사와 문서를 연결.

## 1.8.0

- 사용자가 제공한 group_01 인기 웹소설 TXT 4개를 캘리브레이션해 `reports/group_01_sample_calibration.json` 생성.
- 기존 웹소설/장르 starter 사전의 샘플 확인 항목을 `sample_calibrated`로 승격.
- `lexicons/sample_group_01_terms.ko.json` 추가: 스킬, 보상, 시스템, 마력, 길드, 퀘스트, 게이트, 랭킹 등 샘플 기반 장르 작동어 반영.
- `lexicons/sample_group_01_voice.ko.json` 추가: 서술 어미와 대화 말투 후보를 corpus-level voice marker로 분리.
- `reports/group_01_im_not_ai_alignment.json` 추가: im-not-ai seed 규칙 중 일반 문법형과 S1 차단형을 샘플 기반으로 분리.
- `calibrate_from_samples.py`에 인코딩 fallback과 `--path-mode`를 추가해 외부 샘플 경로를 이식 가능한 파일명 기반 리포트로 저장.

## 1.7.0

- `scripts/calibrate_from_samples.py` 추가: 사용자가 제공할 인기 웹소설 TXT/MD 샘플에서 용어 후보, 말투 후보, im-not-ai 규칙 충돌 후보를 추출.
- 샘플 캘리브레이션 smoke fixture와 리포트 fixture 추가.
- `generate_test_report.py`에 sample calibration smoke 검증 추가.

## 1.6.0

- `lexicons/` 추가: 웹소설 용어, 장르어, 플랫폼 키워드, AI-tell 문구, 금칙어, 캐릭터 보이스 템플릿.
- `schemas/lexicon.schema.json` 추가.
- `scripts/audit_lexicon.py` 추가: 사전 검증 및 원고 내 금칙어/AI-tell 표현 감사.
- local `im-not-ai` taxonomy를 바탕으로 AI-tell/금칙어 seed 작성.
- `generate_test_report.py`, `manifest.json`, `audit_skill_package.py`에 lexicon audit 연결.

## 1.5.0

- `run_manuscript_guard.py` 추가: `$humanize-korean` 적용 확인과 `ai_tell_guard.py --fail-on-s1` 실행/차단 리포트 생성
- `workflow_state.py` 추가: `.omx/state/webnovel-production-workflow.json` phase, loop, iteration, selected failure 저장
- `generate_test_report.py` 추가: export 빌드, 스킬 감사, 프로젝트 검증, 서사 감사, 회귀 테스트를 실행해 `TEST_REPORT.json` 자동 생성
- `update_manifest_checksums.py` 추가: manifest scripts/assets sha256 자동 갱신
- input/output schema 정상·실패 fixture 추가 및 `audit_skill_package.py` schema fixture 검증 강화
- manifest scripts/assets checksum, runtime, network, timeout 감사 강화

## 1.4.0

- Hyperagent 스킬 샘플 필드 기준으로 `manifest.json`, `input.schema.json`, `output.schema.json` 추가
- Codex 로컬 워크플로 스킬에도 `manifest.json` 추가
- `audit_skill_package.py`로 metadata, manifest, export, scripts, references, bundle documents, Codex skill manifest를 전수 감사
- export 번들에 manifest를 포함하고 portable skill package 관점의 검증 명령을 추가

## 1.3.0

- 문장 조립 및 효율적 집필 시스템을 `SENTENCE_ASSEMBLY_SYSTEM.md`로 분리 추가
- `독백 -> 감각적 동적 묘사 -> 호기심 주입` 문장 조립 공정을 Episode Writer와 Narrative Engagement Editor에 반영
- Story before Plot, 핵심 사건 3개, rough outline, 무정지 초고 운영 규칙 추가
- 드라마 클립 15초 정지 묘사 훈련과 선택적 성공작 분석 원칙 추가
- Hyperagent export 번들 문서에 신규 집필 시스템 문서를 포함

## 1.2.0

- 10개 웹소설 작법 소스를 `SERIAL_CRAFT_PRINCIPLES.md`에 내용 탈락 없이 압축·보존
- 1화 전투의 캐릭터 각인·목적·비용·reader-known card 게이트 추가
- 직업·능력 시너지와 주인공 고유 영역을 `Protagonist Advantage Map`으로 구조화
- POV 전환 앵커, 직접/간접 묘사 정책, 회차별 정보 공개 예산 추가
- 1~5 / 5~25 / 25~100 / 100+ 장기 Phase Map과 Scale Ladder 추가
- 5~8화 복선 회수 및 장기 복선 리마인드용 `Foreshadow Ledger` 추가
- 최소/권장/깊은 버퍼와 독자 반응 확인 주기 추가
- `Progression & Foreshadowing Editor` 역할 추가
- 실패 유형 E18~E25 및 결정적 서사 감사·회귀 fixture 추가
- Hyperagent export에 동반 원칙 문서를 포함하도록 빌더 개선


## 1.1.0

- `Narrative Engagement Editor` 역할 추가
- 강도 곡선과 recovery/relationship 회차 규칙 추가
- 감정 고점의 독자 가시적 징검다리 검증 추가
- 1화 주인공 상황·목적·이유·장애물 필드 추가
- 캐릭터 결점의 행동 결과, 관계 영향, 취약성 공개 필드 추가
- 독백 기능, 설명 필요량, 주변 피해, 관계 연속성 필드 추가
- 무대 이동 관계 앵커와 주요 캐릭터 죽음 승인 게이트 추가
- 작가 과부하·고립 위험에 대한 지속 가능성 게이트 추가
- 신규 실패 유형 E9~E17과 회귀 테스트 추가
- `audit_narrative.py` 추가

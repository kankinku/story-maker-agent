# Web Novel Production Loop Skill 1.17.0

Windows PowerShell에서는 검사 전 `$env:PYTHONUTF8=1`을 설정하고 한국어 파일은 `Get-Content -Encoding UTF8`로 읽는다.

웹소설의 시장 조사, 기획, 20화 설계, 비축 집필, 플랫폼 패키징, 연재 운영, 실패 진단과 회귀 테스트를 하나의 인간 승인형 폐쇄 루프로 묶은 AI 에이전트 스킬 패키지입니다.

## 핵심 설계

- `Canonical Story Bible`을 작품 정본으로 사용하고 모든 회차·수정·홍보 문구에 버전을 연결합니다.
- `Engagement And Character System`으로 세계관보다 캐릭터 욕망·선택·관계 차이를 먼저 고정하고, 재미를 10개 근거 기반 차원과 가독성 게이트로 감사합니다.
- `Narrative Control Map`으로 강약, 감정 징검다리, 독자 공개 정보와 관계 앵커를 관리합니다.
- `Opening Contract`로 1화의 주인공 각인·목적·실패 비용과 전투의 서사 기능을 검증합니다.
- `Protagonist Advantage Map`으로 이전 직업, 능력 시너지, 고유 영역의 독점 경계·비용·증명 회차를 관리합니다.
- `POV & Exposition Policy`로 시점 전환 앵커, 직접/간접 묘사 모드, 회차별 설명 예산을 고정합니다.
- `Foreshadow Ledger`로 복선의 seed·reminder·payoff를 추적하고, `Phase Map + Scale Ladder`로 각인→성장→관계→스케일의 장기 전개를 관리합니다.
- 버퍼는 최소 출시선·권장선·깊은 버퍼로 나누고, 댓글·지표를 정해진 리뷰 주기에만 정본 변경 근거로 사용합니다.
- 실패는 `Trace → Diagnose → Patch Proposal → Human Approval → Replay → Regression Lock` 순서로 처리합니다.

## 빠른 실행

```bash
python scripts/audit_skill_package.py --project-root ..
python scripts/validate_project.py tests/fixtures/valid_project.json
python scripts/audit_narrative.py tests/fixtures/valid_project.json
python scripts/run_engagement_contract_tests.py
python scripts/run_semantic_rubric_tests.py
python scripts/audit_workspace_projects.py --project-root ..
python scripts/run_portable_export_tests.py
python scripts/run_regression.py tests/regression_cases.json
python scripts/build_export.py --output dist/webnovel-production-loop.skill.json
python scripts/generate_test_report.py --project-root ..
```

Lexicon validation is included in the generated test report. To audit a manuscript directly:

```bash
python scripts/audit_lexicon.py --manuscript path/to/manuscript.txt
```

S1 AI-tell or prohibited phrase hits should block manuscript completion unless the span is a protected quote, proper noun, numeric fact, legal citation, or explicit in-world term.

When current popular webnovel TXT/MD samples are supplied, derive candidate dictionary updates without copying source prose:

```bash
python scripts/calibrate_from_samples.py samples/popular --output sample_calibration_report.json
```

To transplant a sample's structure into a reusable style profile and check a draft:

```bash
python scripts/calibrate_from_samples.py samples/popular --output sample_calibration_report.json --path-mode basename
python scripts/audit_style_profile.py drafts/episode_01.txt --profile templates/style_profile.json
python scripts/run_semantic_rubric.py templates/chapter_audit.json --include-style
```

For dimension-transfer survival expedition projects, use the dimension-survival references before planning or drafting:

```text
references/dimension-survival/survival-expedition-loop.md
references/dimension-survival/resource-choice-and-conversion.md
references/dimension-survival/procedural-exposition.md
references/dimension-survival/utility-to-trust-relationship.md
references/styles/dimension-survival-expedition.md
```

For transcendent-gallery or vampire-retainer samples, keep the engines separate:

```text
references/transcendent-gallery/
references/styles/transcendent-gallery-climb.md
references/vampire-retainer/
references/styles/vampire-retainer-misunderstanding.md
```

## 주요 디렉터리

- `SKILL.md`: 런타임 운영 규격과 승인 게이트
- `manifest.json`: portable skill package 라우팅, 권한, 입력·출력 schema, 전체 런타임 자산 체크섬, 검증 명령
- `ARCHITECTURE.md`: 다중 에이전트, 정본, 상태 머신, 자기수복 구조
- `NARRATIVE_PRINCIPLES.md`: 창작 원칙과 시스템 요소의 매핑
- `SERIAL_CRAFT_PRINCIPLES.md`: 추가 10개 작법 소스의 내용 보존형 정리
- `SENTENCE_ASSEMBLY_SYSTEM.md`: 문장 조립, 영상 클립 훈련, Story/Plot 분리, 선택적 분석, 무정지 집필 지침
- `ENGAGEMENT_CHARACTER_SYSTEM.md`: 캐릭터 우선 정본, 장면 진행 계약, 10개 재미 차원, 화 단위 만족과 가독성 게이트
- `SAMPLE_STYLE_PROTOCOL.md`: 샘플 기반 문체·연출 구조를 style profile, scene contract, draft, audit로 이식하는 지침
- `sources/`: 사용자 제공 원문 보존
- `templates/source_remake_blueprint.json`: 원문에서 추출·추상화한 설정을 승인하고 Writer 입력을 원문과 격리하는 리메이크 블루프린트
- `references/dimension-survival/`: 제한시간형 차원 원정, 자원 선택, 절차 설명, 실용적 동료 관계 reference
- `references/transcendent-gallery/`: distributed mentor feedback, evidence-based combat review, one-life tower progression, gallery emotional chorus reference
- `references/vampire-retainer/`: evidence-based misunderstanding, delegated combat, retainer growth economy, supernatural domestic comedy reference
- `metadata.json`: 라우팅·태그·export 메타데이터
- `config/`: 평가 정책, 실패 분류, 플랫폼 프로필
- `schemas/`: 입력·출력·프로젝트·Trace·회귀 사례 JSON Schema
- `prompts/`: 역할별 에이전트 지침
- `templates/`: 프로젝트·Story Bible·회차·주간 리뷰·style profile·scene contract·chapter audit·dimension/inventory/equipment·mentor/stage/retainer/reputation/hidden identity 템플릿
- `scripts/`: 스킬 패키지 감사, 결정적 검증, 서사 감사, 회귀 실행, 원고 guard, workflow state, checksum, test report, export 빌드
- `tests/`: 정상·실패 fixture와 회귀 사례
- `dist/`: 문서·스크립트·config·schema·template·prompt·lexicon·reference를 포함한 단일 Skill JSON

Portable 검사는 package-internal validator만 격리 실행합니다. 역사 샘플 overlay와 legacy runner 검사는 `run_context_compounding_tests.py --project-root <workspace>`로 실행하는 workspace integration 범위입니다.

## 현재 검증 범위

1. 20화 계획, 초반 hook, 결말 방향, 출시 메타데이터와 버퍼
2. 1화 전투의 목적·비용·독자 사전 정보
3. 직업·능력 시너지와 고유 영역의 경계·비용·증명 회차
4. POV 전환 앵커와 회차별 신규 정보 예산
5. 8화를 넘는 복선의 리마인드 계획
6. 네 단계 Phase Map과 Scale Ladder
7. 작가 반응 확인 주기, 버퍼 정책, 고립 위험
8. 문장 조립 블록, Story before Plot, 핵심 사건 3개와 무정지 초고 운영
9. 샘플 스타일 프로필의 문단 리듬, 정보 채널, 화말 열린 고리 감사
10. 1~5 의미 루브릭 점수 검증
11. 차원이동 생존 원정물의 결핍·원정·파밍·귀환·재가공·새 병목 구조화
12. 초월자 갤러리형 탑 등반물의 다중 멘토 피드백·증거 리뷰·1회성 층 공략·갤러리 정서 코러스 구조화
13. 권속 경영형 착각 코미디의 증거 기반 오해·위임 전투·권속 성장 경제·초자연 일상 코미디 구조화
14. 해시 결합 원문·재작성 계약의 사건 누락·추가·순서·고유명사·보호 인용문 충실도 검사
15. 원본 리메이크의 `source lock -> extract -> abstract -> blueprint approval -> rebuild -> draft -> isolated compare` 입력 격리
15. portable manifest checksum, input/output schema fixture, Codex workflow manifest, 자동 TEST_REPORT 생성

# Narrative Principles Mapping

사용자가 제공한 「웹소설 창작 핵심 원칙 분석 보고서」를 시스템 구성 요소로 변환한 매핑 문서다.

| 창작 원칙 | 시스템 반영 위치 | 검증 방식 |
|---|---|---|
| 에피소드 강약과 완급 | Narrative Control Map, Episode `mode/intensity` | 고강도 연속 상한, recovery/relationship 존재 |
| 감정의 단계적 축적 | Episode `emotion_bridges` | 감정 고점 최소 bridge 수 |
| 초반 상황·목적 제시 | Concept와 1화 Episode 필드 | situation/goal/obstacle 필수 |
| 결점과 유대감 | Character schema | behavioral consequence, vulnerability reveal, relationship effect |
| 독백과 동지화 | Episode `monologue_function` | 1~3화 기능 필수, 의미 평가 |
| 개연성과 주변 피해 | Episode `collateral_risk` | 의미 감사 + 실패 분류 E14 |
| 무대 이동 관계 유지 | Episode `stage_transition`, `relationship_continuity` | 전환 시 관계 앵커 필수 |
| 캐릭터 죽음 위험 | Episode `death_event` | 승인·서사완결·대체보상 필수 |
| 작가 상태와 관계 관리 | Author Sustainability Profile, Weekly Review | critical load/isolation launch block |
| 레고 블록형 문장 조립 | Episode Writer, Sentence Assembly System | 독백 기능, 동적 묘사, 호기심 주입 체크 |
| 영상 클립 묘사 훈련 | Writer Training Loop | 15초 단위 행동·대사·배경 문장화 |
| Story before Plot | Story Architect | 결핍·욕구·내면 변화 없이 사건표 진행 금지 |
| 선택적 성공작 분석 | Market Researcher, Serial Ops | 장르별 1~2개 분석 대상, 최신성 확인 |
| 무정지 초고와 핵심 사건 3개 | Draft Buffer, Phase Map | rough outline, anchor events, 후속 검증 루프 |
| 캐릭터 우선 시놉시스 | Story Bible character-first fields, Logline | 세계 규칙 전에 욕망·비용·원칙·선택 방식·반복 매력 존재 |
| 추상적 재미의 구체화 | Engagement Rubric, Chapter Audit | 10개 차원별 1~5 점수와 장면 근거 |
| 모든 장면의 진행성 | Scene Contract | plot/character/relationship/world_rule_in_use 중 하나 이상 |
| 화 단위 만족과 다음 동력 | Episode Contract | 해결 질문·상태 변화·독자 보상·다음 구체 질문의 인과 |

## 핵심 설계 판단

1. 이 원칙들은 단순 문체 팁이 아니라 **정본 데이터와 승인 게이트**로 관리한다.
2. 감정·몰입 검사는 설정 일관성과 다른 문제이므로 `Narrative Engagement Editor`를 별도 역할로 둔다.
3. 강약·징검다리·관계 앵커처럼 구조화 가능한 항목은 결정적 검증으로 고정한다.
4. 감정의 설득력, 독백의 자연스러움, 캐릭터 애착처럼 확률적인 항목은 LLM 평가와 사람 검토를 함께 사용한다.
5. 주요 죽음·영구 이별·관계 전면 교체는 자동 최적화 대상이 아니라 고위험 창작 의사결정으로 취급한다.
6. 캐릭터 배경 분량, 빙의·환생 사용, 초반 회차 수치는 획일적 강제가 아니라 기능과 대체 보상을 요구하는 휴리스틱으로 취급한다.

상세한 캐릭터 우선 정본, 장면 계약, 재미 평가 차원과 예외는 `ENGAGEMENT_CHARACTER_SYSTEM.md`를 참조한다.


## 추가 10개 소스의 시스템 매핑

| 소스 원칙 | 정본/에이전트 반영 | 결정적 검사 또는 감사 |
|---|---|---|
| 1화 전투보다 캐릭터 각인 | Opening Contract, Narrative Engagement Editor | combat이면 목적·비용·reader-known card 필수 |
| 반응 독립성과 깊은 비축분 | Author Sustainability Profile, Serial Ops | 출시 최소선·권장선 분리, 반응 확인 주기 |
| 캐릭터 서사 우선 정보 공개 | Exposition Policy | 현재 장면 필수 정보와 지연 정보 분리 |
| 직접 묘사 기본·하이라이트 간접 묘사 | Description Policy | 평시/절정 mode 대비 감사 |
| 직업과 능력의 시너지 | Protagonist Advantage Map | 직업 전문성의 1~25화 증명 장면 |
| 1인칭 주시점과 명확한 전환 | POV Contract | 무표지 POV 전환 차단 |
| 각인→성장→관계→스케일 | Long-form Phase Map | 구간별 목표와 증명 장면 존재 |
| 5~8화 복선 회수와 리마인드 | Foreshadow Ledger | 8화 초과 gap이면 reminder 필수 |
| 침범 불가능한 고유 영역 | Unique Domain Spec | 경계·비용·반복 보상·복제 위험 검사 |
| 관계와 인물 격의 동시 상승 | Scale Ladder | arena·authority·decision impact 상승 |

상세한 소스별 원칙과 예외는 `SERIAL_CRAFT_PRINCIPLES.md`를 참조한다.

## 문장 조립 및 효율적 집필 시스템 매핑

상세 운용 지침은 `SENTENCE_ASSEMBLY_SYSTEM.md`를 참조한다.

| 공정 | 적용 에이전트 | 산출물 |
|---|---|---|
| Internal Monologue | Episode Writer, Narrative Engagement Editor | 상황 정리, 위험 평가, 목표, 선택 근거 |
| Sensory Description | Episode Writer | 동적 동사, 감각 묘사, 문장 리듬 |
| Curiosity Injection | Narrative Engagement Editor, Continuity Editor | 미공개 카드, 정보 격차, 다음 질문 |
| Drama Clip Training | Episode Writer | 15초 장면 문장화 훈련 노트 |
| Story/Plot 분리 | Story Architect | 결핍·욕구·내면 변화와 사건 인과 분리 |
| Style Targeting | Market Researcher, Serial Ops | 분석 대상 1~2개와 흡수 포인트 |
| Nonstop Draft | Episode Writer, Orchestrator | 러프 초고와 후속 검증 루프 |

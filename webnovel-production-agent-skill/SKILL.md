# Web Novel Production Loop

아이디어와 작가의 제약을 받아 **시장 가설 -> 작품 정본 -> 20화 설계 -> 비축 원고 -> 플랫폼 패키징 -> 연재 운영 -> 실패 진단 -> 수정 검증 -> 회귀 테스트 축적**까지 수행하는 웹소설 제작·운영 스킬이다.

이 스킬의 목적은 원고를 대신 무한 생성하는 것이 아니다. 작가가 완결 가능한 작품 시스템을 만들고, 운영 중 발생한 실패를 다음 실행의 품질 자산으로 바꾸는 것이다.

## Purpose

- 막연한 아이디어를 연재 가능한 기획 패키지로 변환한다.
- 설정, 캐릭터, 결말 방향, 회차 계획을 하나의 정본으로 관리한다.
- 서사의 강약, 감정의 징검다리, 독자에게 공개된 정보량, 시점·묘사, 복선, 고유 영역과 관계 연속성을 별도 제어면으로 관리한다.
- 주인공의 현재 상황·목적·장애물을 초반에 명확히 제시하고 독백·행동을 통해 독자와의 동지화를 만든다.
- 문장은 `독백 -> 감각적 동적 묘사 -> 정보 은닉/질문`의 조립 공정으로 생산하고, 초고는 무정지 작성 후 검증 루프에서 다듬는다.
- 샘플 기반 문체는 원문 문장 모사가 아니라 정보 채널, 문단 리듬, 기대-반전-보상, 반복 도전 루프 같은 연출 결정을 추출해 `style profile -> scene contract -> draft -> audit`로 적용한다.
- 초반 후킹, 회차 말미, 비축분, 메타데이터를 출시 전에 검증한다.
- 플랫폼별 포장 전략을 최신 공식 정보와 현재 노출면에 맞춰 갱신한다.
- 운영 실패를 추적하고 최소 수정안으로 복구한 뒤 회귀 테스트로 잠근다.
- 계약과 저작권 위험은 자동 승인하지 않고 인간 검토로 에스컬레이션한다.

## When to use

다음 요청에 사용한다.

- "웹소설 아이디어를 연재 가능한 기획으로 만들어줘"
- "세계관, 캐릭터, 20화 사건표를 같이 설계해줘"
- "1~5화 시놉시스와 초반 후킹을 점검해줘"
- "10화 비축분을 만들고 연재 일정까지 잡아줘"
- "네이버/문피아/카카오/조아라에 맞게 제목과 소개를 바꿔줘"
- "연재 지표와 댓글을 보고 다음 화를 어떻게 고칠지 분석해줘"
- "설정 충돌이나 독자 이탈 원인을 추적하고 재발 방지 테스트를 만들어줘"

다음 경우에는 사용하지 않는다.

- 사용자가 완성된 원고 한 문단의 단순 맞춤법 교정만 원하는 경우
- 저작권 계약의 법률적 결론이나 서명을 대신 요구하는 경우
- 원작 허락이 확인되지 않은 팬픽·2차 창작의 상업화 실행을 요구하는 경우
- 특정 현존 작가의 고유 문체를 그대로 복제하려는 경우

## Required inputs

### 최소 입력

1. 장르 또는 장르 후보
2. 한 줄 콘셉트 또는 아이디어 메모
3. 목표: 완결 경험 / 테스트 연재 / 공모전 / 유료화 중 우선순위
4. 작가가 실제로 확보할 수 있는 주간 집필 시간

### 권장 입력

- 목표 독자와 감정적 보상
- 선호·금지 소재
- 목표 플랫폼 후보
- 예상 총화수 또는 시즌 길이
- 참고작 2~3개와 참고하려는 요소
- 이미 작성한 원고, 설정집, 댓글·지표

정보가 부족해도 가설안은 만들 수 있지만, **장르·독자·작품 약속·결말 방향**을 확정하기 전에는 대량 집필로 넘어가지 않는다.

## Output contract

한 프로젝트의 기본 산출물은 다음으로 고정한다.

1. `project.json`: 상태, 목표, 플랫폼 가설, 연재 계획
2. `story_bible.json`: 세계 규칙, 캐릭터, 핵심 갈등, 결말 방향
3. `episode_plan.json`: 최소 20화 사건표와 화별 클리프행어
4. `launch_package.json`: 제목, 한줄소개, 긴소개, 태그, 연령등급, 공지
5. `episodes/`: 승인된 회차 원고와 편집 이력
6. `traces/`: 모델·프롬프트·도구·입출력·평가 기록
7. `reviews/`: 주간 지표·댓글 분석과 유지/수정/폐기 결정
8. `regressions/`: 실제 실패 입력, 기대조건, 수정 전후 결과
9. `style_profiles/`: 샘플에서 파생된 문단 리듬, 정보 채널, 마이크로 비트, 금지 패턴
10. `scene_contracts/`: 회차별 상태 변화, 기대, 반전, 독자 보상, 화말 열린 고리, 장면 비트
11. `dimension_states/`: 차원이동 생존 원정물의 차원 계약, 인벤토리, 장비 의존성, 미회수 위협
12. `mentor_states/`: 초월자 갤러리형 탑 등반물의 멘토 전문성, 조언 충돌, 층계 기록, 외부 평판
13. `retainer_states/`: 권속 경영형 착각 코미디의 권속 등록부, 혈력 경제, 평판 오해, 숨은 정체 관계
14. `context/`: 작업별 Context Plan과 출처·버전·권위·최신성이 포함된 Evidence Pack
15. `character_states/`와 `relationship_states/`: 회차별 구조화 상태 스냅샷과 승인된 Episode Memory Delta
16. `reviews/`: 명시적 초안/최종본 Review Packet과 의미 단위 Review Diff
17. `proposals/`: 반복 패턴에서 생성된 Change Proposal, Replay, Canary, Rollback 기록

모든 산출물은 `project_id`, `project_version`, `story_bible_version`을 공유해야 한다.

## Core invariant

> 모든 회차, 수정안, 홍보 문구, 운영 판단은 승인된 `Canonical Story Bible`과 현재 `Project Version`에서 파생되어야 한다. 캐릭터 욕망, 세계 규칙, 결말 방향, 작품 약속을 바꾸는 수정은 자동 적용하지 않고 명시적 change set과 작가 승인을 요구한다.

이 원칙은 장기 연재에서 설정 드리프트와 즉흥적 독자 반응 추종을 막는 기준이다.

### Narrative invariants

1. **강한 장면은 대비가 있을 때만 강하다.** 고강도 사건을 연속 배치하지 않고 회복·관계·일상 회차를 계획한다.
2. **감정은 독자가 아는 정보만큼만 폭발할 수 있다.** 감정 고점 전에는 행동, 손실, 망설임, 선택으로 징검다리를 축적한다.
3. **초반의 우선순위는 세계관이 아니라 방향성이다.** 1화 안에 주인공의 정체, 현재 상황, 목적, 핵심 장애물을 파악할 수 있어야 한다.
4. **결점은 선택에 비용을 만들어야 한다.** 캐릭터 결점과 상처는 설명용 속성이 아니라 행동과 관계를 실제로 왜곡해야 한다.
5. **독백은 독자와 주인공의 판단을 연결한다.** 상황·목표·선택 근거를 공유하되 같은 형식의 설명 독백을 반복하지 않는다.
6. **선한 의도만으로 개연성이 확보되지 않는다.** 주변 피해, 책임 소재, 대안, 피해 완화 노력을 함께 검토한다.
7. **무대 이동 시 관계의 연속성을 보존한다.** 기존 핵심 인물과의 접점을 모두 끊지 않는다.
8. **주요 캐릭터의 죽음은 충격이 아니라 서사의 완결이어야 한다.** 핵심 보상 관계를 파괴하는 죽음은 별도 승인과 대체 정서 보상 설계를 요구한다.
9. **작가의 지속 가능성은 작품 외부 변수가 아니다.** 과부하·고립 신호가 있으면 연재 속도보다 회복과 소통 계획을 우선한다.
10. **1화의 전투는 목적과 카드가 보일 때만 작동한다.** 캐릭터 각인·승패 비용·독자가 아는 정보가 없는 공방은 차단한다.
11. **세계관은 주인공의 인생과 현재 문제를 통해 공개한다.** 당장 생존과 선택에 필요하지 않은 스케일 설명은 지연한다.
12. **묘사는 장면 기능에 따라 배분한다.** 평시는 직접 묘사로 명료성을 확보하고, 하이라이트에서 간접 묘사를 제한적으로 사용한다.
13. **직업은 능력의 사용법을 바꿔야 한다.** 이력은 명찰이 아니라 전문성·오판·활약 기대를 생산해야 한다.
14. **시점 전환에는 경계 표지가 필요하다.** 1인칭 또는 3인칭 선택보다 독자가 현재 인식 주체를 잃지 않는 것이 우선이다.
15. **장기 연재의 중심 과업은 이동한다.** 1~5화 각인, 5~25화 성장 증명, 25~100화 관계 심화, 100화 이후 스케일 확장을 관리한다.
16. **복선은 독자의 망각을 전제로 설계한다.** 짧은 복선은 5~8화 내 회수하고 장기 복선은 회수 시 리마인드를 제공한다.
17. **주인공에게 침범하기 어려운 고유 영역이 있어야 한다.** 경계·비용·반복 보상을 함께 설계해 만능 치트와 평준화를 피한다.
18. **스케일업은 적의 숫자만 높이는 일이 아니다.** 주인공이 만나는 인물의 권력, 접근 권한, 결정 영향 범위가 함께 상승해야 한다.
19. **독자 반응은 집필 명령이 아니라 관측 데이터다.** 정본과 버퍼를 보호하기 위해 반응 확인과 수정 결정을 주간 단위로 묶는다.

## Canonical specs

### 작품 콘셉트

- 한 줄을 넘지 않는다.
- `주인공/상황 + 비정상적 변화 + 반복적으로 제공할 재미`가 드러나야 한다.
- 장르 표시는 별도 필드로 관리한다.

### 작품 약속

독자가 1~5화 안에 확인할 수 있는 보상을 한 문장으로 정의한다.

예: "몰락한 회계사가 이세계 왕국의 장부를 고쳐 권력 구조를 뒤집는 과정에서, 매 화 숫자로 위기를 해결하는 쾌감을 준다."

### 세계관

설명문이 아니라 다음 형태로 기록한다.

- 규칙
- 예외
- 규칙이 만드는 비용
- 규칙을 둘러싼 이해관계
- 독자에게 공개되는 시점

### 캐릭터

최소 필드:

- 욕망
- 결핍
- 상처
- 숨긴 비밀
- 도덕적 약점
- 행동 패턴
- 말투 표지
- 시즌 시작과 종료 상태


### 주인공 상황 삼각형

초반 정본에는 다음 네 항목을 별도 필드로 고정한다.

- 현재 상황: 지금 주인공에게 이미 벌어진 문제
- 구체 목적: 다음 몇 화 동안 실제로 하려는 일
- 목적의 이유: 실패할 수 없는 개인적 근거
- 핵심 장애물: 행동을 막는 외부·내부 저항

성격 형용사보다 이 네 항목이 독자가 작품을 따라갈 방향을 결정한다.

### 캐릭터 내면과 관계

캐릭터는 기본 설정 외에 다음을 기록한다.

- 결점이 실제 선택을 왜곡하는 방식
- 상처가 현재 관계에 미치는 영향
- 진심 또는 취약성을 공개할 예정 장면
- 핵심 관계의 시작 상태와 목표 상태
- 무대 이동 시 유지해야 할 관계 앵커

### 서사 강도와 감정 제어

- 각 회차는 `1~5`의 강도와 `setup / pressure / payoff / recovery / relationship / transition` 모드를 가진다.
- 고강도 회차가 연속되면 회복 또는 관계 회차를 배치한다.
- 감정 고점은 최소 두 개 이상의 선행 징검다리를 요구한다.
- 독자가 아직 모르는 정보를 감정의 전제로 사용하지 않는다.
- 하이라이트가 시작된 뒤에는 긴 설명과 회상을 삽입하지 않는다.

### 독자 정렬과 정보 공개

- 1~3화에는 주인공의 판단을 이해할 수 있는 독백 또는 대화 기능이 있어야 한다.
- 독백은 상황 정리, 위험 평가, 목표, 선택 근거 중 하나의 명시적 기능을 가진다.
- 설정은 `현재 장면 이해에 필요한가`를 기준으로 공개한다.
- 독자가 아는 사실과 캐릭터가 아는 사실을 분리 기록한다.

### 문장 조립 공정

초고 문장은 완성형 문장을 한 번에 만들지 않고 다음 블록으로 조립한다.

1. `Internal Monologue`: 주인공의 주관적 평가, 위험 판단, 목표, 선택 근거를 배치한다.
2. `Sensory Description`: 분위기와 행동을 감각으로 붙이고 정적 설명보다 동적 동사를 사용한다.
3. `Curiosity Injection`: 핵심 정보 일부를 보류해 다음 질문, 비용, 미공개 의도, 정보 격차를 만든다.

평면적 행동 나열은 이 세 블록 중 빠진 기능을 찾아 보강한다. 정보 은닉은 독자를 속이는 누락이 아니라 장면의 다음 행동을 궁금하게 만드는 설계여야 한다.

### 샘플 스타일 제어

샘플 문체는 다음 네 단계로만 사용한다.

1. `style_extractor`: 문장 복사가 아니라 문단 길이, 정보 채널, 마이크로 비트, 도전 루프, 안티패턴을 추출한다.
2. `scene_planner`: 추출된 규칙을 회차 계약과 장면 카드로 변환한다.
3. `chapter_writer`: 승인된 정본과 장면 계약 안에서 원고를 쓴다.
4. `reviser`: 구조 감사, 루브릭, lexicon, manuscript guard로 결과를 검증한다.

샘플의 고유 문장, 농담, 명칭, 사건 배열은 재사용하지 않는다. 반복 사용 가능한 것은 `언제 적용하는가`, `어떤 순서로 실행하는가`, `무엇을 피하는가`, `어떻게 검증하는가`로 정리된 작동 규칙이다.

기본 정보 채널은 다음처럼 구분한다.

- `narration`: 주관적 해석, 위험 평가, 자기합리화
- `dialogue`: 관계 압력, 정보 교환, 캐릭터 목소리
- `system`: 객관적 규칙, 보상, 비용, 상태 변화
- `community`: 반응, 해설, 반론, 개그, 복선
- `action`: 관찰, 가설, 시도, 결과, 재도전

장면 비트는 `상황 -> 주인공 해석 -> 기대 -> 반전 -> 짧은 감정 반응 -> 새 행동 목표`를 기본형으로 삼되, 모든 장면에 기계적으로 채우지 않는다. 누락된 비트가 있으면 의도적 생략인지 추진력 실패인지 감사한다.

### 차원이동 생존 원정 엔진

차원이동 샘플을 다룰 때 핵심은 이동 자체가 아니라 `결핍 -> 제한시간 원정 -> 선택형 파밍 -> 귀환 후 재가공 -> 거점 개선 -> 새 병목`이다. 이 유형은 `references/dimension-survival/`와 `references/styles/dimension-survival-expedition.md`를 사용한다.

필수 제어면:

- `survival-expedition-loop`: 본래 세계 결핍, 원정 목표, 시간·적재 제한, 귀환 후 개선.
- `resource-choice-and-conversion`: 모든 자원을 가져가지 못하게 만드는 선택, 포기, 교체, 후순위 지정.
- `procedural-exposition`: 시스템·전문가·주인공의 설명 역할 분리와 행동으로의 번역.
- `utility-to-trust-relationship`: 실용적 조력자가 신뢰와 감정 관계로 발전하는 단계.

차원별 계약은 다음을 가져야 한다.

- 시각적 정체성
- 상시 환경 위험
- 적의 행동 원리
- 이 차원에서만 얻는 자원 범주
- 멸망 원인 또는 현지 비극
- 이 차원에서 반복할 핵심 행동 동사

보상 규칙:

- 새 능력과 장비는 새 자유를 주면서 유지비, 전력, 부품, 보호 책임, 재방문 위험 같은 병목을 만든다.
- 좋은 전리품은 즉시 사용, 본래 세계 재가공, 다음 원정 선택지 확대의 세 단계 중 둘 이상을 수행한다.
- 귀환 장면은 인벤토리 정산이 아니라 생활 조건 변화, 장비 제작, 새 병목 발견, 본래 세계 감정선 진전을 포함해야 한다.

### 초월자 갤러리 멘토형 탑 등반 엔진

초월자 갤러리형 샘플은 커뮤니티 댓글이 많은 문체가 아니라 `단 한 번의 생존 등반에서 복수 멘토의 불완전한 조언을 수집하고 주인공이 자기 조건에 맞게 변형하는 성장물`이다. 이 유형은 `references/transcendent-gallery/`와 `references/styles/transcendent-gallery-climb.md`를 사용한다.

필수 제어면:

- `distributed-mentor-feedback`: 최소 두 멘토의 관점, 조언의 전제와 한계, 주인공의 선택·변형.
- `evidence-based-combat-review`: 사진·영상 업로드가 새 실수, 성공 원인, 재현 조건, 숨은 위험을 제공.
- `one-life-tower-progression`: 실패 반복이 아니라 사전 정보, 훈련, 관찰, 타인의 경험, 순간 결단으로 한 번뿐인 공략을 통과.
- `gallery-emotional-chorus`: 갤러리가 관전석에서 정서적 공동체와 상담가 역할로 확장.

갤러리 댓글은 감탄 코러스가 아니라 분석, 반론, 개그, 경고, 정서 지원 중 하나의 기능을 가져야 한다. 외부 시점은 주인공 칭찬용이 아니라 초월갤 내부 평가와 바깥 평판의 차이를 만들어 새 갈등을 발생시켜야 한다.

### 권속 경영형 착각 코미디 엔진

흡혈귀 권속형 샘플은 강한 주인공이 직접 싸우는 헌터물이 아니라 `생활에는 불편하고 연약한 주인공이 권속을 전략적으로 운용하고, 외부가 관찰 가능한 증거를 바탕으로 보이지 않는 주군을 과대평가하는 착각 코미디`다. 이 유형은 `references/vampire-retainer/`와 `references/styles/vampire-retainer-misunderstanding.md`를 사용한다.

필수 제어면:

- `evidence-based-misunderstanding`: 실제 의도, 외부 관찰 정보, 합리적 추론, 소문 인플레이션.
- `delegated-combat-and-agency`: 권속이 전투를 맡아도 주인공은 조사, 배치, 자원 배분, 구조 우선순위, 평판 대응을 결정.
- `retainer-growth-economy`: 혈력, 피의 정수, 소환 쿨타임, 권속 슬롯, 장비, 영지, 정보가 선택 비용을 만든다.
- `supernatural-domestic-comedy`: 고귀한 정체가 일상 제약과 내면/외부 말투 충돌로 반복 코미디를 만든다.

착각은 말투 하나로 발생하면 안 된다. 권속의 힘, 충성 표현, 주인공의 부재, 시스템 명칭, 세계급 사건의 흔적처럼 외부가 실제로 관찰한 근거가 있어야 한다.

### 고위험 서사 장치

다음은 자동 적용하지 않는다.

- 핵심 관계의 영구 단절
- 메인 보상 캐릭터의 죽음
- 무대 이동과 동시에 기존 인물 전원 이탈
- 주인공의 선행이 대규모 주변 피해를 만드는 선택
- 독자가 기대한 핵심 관계 보상의 철회

각 장치는 인과, 대안, 독자 보상, 관계 후속 계획과 사람 승인을 요구한다.


### Opening Contract와 1화 전투 게이트

- 1화는 주인공 각인, 현재 상황, 당장 목적, 실패 비용을 우선한다.
- 1화가 전투라면 `전투의 서사 기능`, `승패 비용`, `독자가 미리 아는 카드`, `적과의 정보 격차`를 기록한다.
- 전투가 목적을 생성하는 패배·배신·굴욕의 후속 장면이면 `aftermath`로 구분한다.
- 단순한 기술 공방이나 독자가 모르는 능력으로 갑자기 승리하는 장면은 출시 게이트를 통과하지 못한다.

### Protagonist Advantage Map

주인공의 직업·능력·고유 영역을 다음처럼 관리한다.

- 이전 직업 또는 장기 경험
- 전이 가능한 전문 지식과 행동 습관
- 새 능력과의 시너지
- 주인공만 접근 가능한 고유 영역
- 타인이 침범할 수 없는 경계와 예외
- 사용 비용, 한계, 오판 가능성
- 1~25화 안에 전문성과 고유 영역을 증명할 장면
- 타인의 리스펙과 정보 격차가 발생할 대상

### POV·묘사 계약

- 프로젝트의 주시점과 허용 변형, 시점 앵커, 전환 표지를 정본으로 고정한다.
- 장면별 인식 주체를 기록하고 무표지 시점 전환을 금지한다.
- 1인칭에서는 연속적인 `나는` 반복을 피하되, 주체가 모호해지면 생략보다 명료성을 우선한다.
- 평시 묘사 기본값과 하이라이트 묘사 모드를 분리한다. 기본은 직접적·직관적 전달, 절정은 행동·이미지·배경 비유를 통한 제한적 간접 묘사다.

### Exposition Policy

- 설정 공개 기준은 `현재 장면의 선택과 위험을 이해하는 데 필요한가`다.
- 생존 규칙과 즉시 행동 조건은 초반에 공개한다.
- 제국 전체 역사, 먼 지역 세력, 현재 갈등에 영향이 없는 스케일 정보는 지연한다.
- 회차별 신규 규칙·고유명사·세력의 설명 예산을 두고 초과 시 분산한다.

### Long-form Phase Map

- `1~5화`: 주인공 각인, 현재 상황, 목적, 고유 영역의 기대를 만든다.
- `5~25화`: 직업·능력 시너지와 성장 방식을 반복적으로 증명한다.
- `25~100화`: 핵심 조연의 내면과 관계를 깊게 만들어 장기 애착을 확보한다.
- `100화 이후`: 기존 성장 엔진을 더 큰 무대·권력자·기관에 적용해 사회적·권력적 스케일을 높인다.

### Foreshadow Ledger

복선마다 다음을 기록한다.

- seed 회차와 장면
- explicit / hidden 가시성
- 독자가 기억해야 할 핵심 문장·이미지·행동
- 예상 payoff 회차
- 8화를 넘길 경우 reminder 계획
- 회수 결과와 새로운 질문

### Scale Ladder

- 활동 무대의 범위
- 적과 동료의 힘 또는 권력 등급
- 주인공이 접근 가능한 기관·인물
- 주인공의 사회적 위치
- 결정이 영향을 미치는 사람과 지역의 범위
- 기존 핵심 관계가 확장된 무대에서 맡는 새로운 역할

### 20화 사건표

각 화는 다음 필드를 가진다.

- 화의 목표
- 주인공의 선택
- 저항 또는 비용
- 정보 변화
- 감정 변화
- 작품 약속의 제공 방식
- 마지막 질문 또는 클리프행어
- 회차 모드와 강도
- 주인공의 현재 상황과 이번 화 목적
- 독자가 이미 알고 있어야 하는 사실
- 감정 고점의 징검다리
- 독백 또는 대화의 정보 전달 기능
- 설명이 필요한 최소 정보
- 주변 피해와 책임 검토
- 관계 연속성 및 무대 이동 여부
- 장면 시점과 전환 표지
- 평시/하이라이트 묘사 모드
- 신규 설정·고유명사 설명 예산
- 전투라면 서사 기능, 승패 비용, 독자에게 공개된 카드
- 직업·능력·고유 영역 증명 방식
- 복선 seed/payoff/reminder ID
- 장기 구간과 scale ladder 단계
- 문장 조립 초점: 독백 기능, 동적 묘사 대상, 은닉 정보 또는 다음 질문

## Agent topology

### 1. Orchestrator

프로젝트 상태, 승인 게이트, 정본 버전, 작업 순서를 관리한다. 직접 장문 원고를 생성하기보다 적절한 역할 에이전트에 작업을 배분한다.

### 2. Market Researcher

공식 플랫폼 가이드, 현재 랭킹·노출면, 공모전·정책을 조사한다. 추천 알고리즘을 추측하지 않으며, 공식 사실과 실무 가설을 분리한다.

### 3. Story Architect

캐릭터 우선 정본, 로그라인, 콘셉트, 장르, 작품 약속, 주인공 상황 삼각형, 캐릭터 결점·관계, 최소 세계 규칙, 결말 방향, 20화 사건표와 강도 곡선을 설계한다. `ENGAGEMENT_CHARACTER_SYSTEM.md`에 따라 세계관보다 욕망·실패 비용·선택 방식·반복 매력을 먼저 고정한다.

### 4. Episode Writer

승인된 회차 계획을 장면 단위로 확장하고 초안을 만든다. 정본을 바꿔야 할 필요가 생기면 원고에 몰래 반영하지 않고 change request를 만든다.

### 5. Narrative Engagement Editor

강약 대비, 감정 징검다리, 독자 정보량, 주인공-독자 정렬, 설명 타이밍, 주변 피해, 관계 연속성과 캐릭터 죽음 위험을 감사한다. 문장 취향이 아니라 캐릭터 매력·주도성·목표·축적 보상·완급·페이싱·설정 전달·화 단위 완결·관계 케미·다음 화 질문의 인과를 장면 근거로 검토한다.

### 6. Progression & Foreshadowing Editor

각인→성장→관계→스케일의 장기 구간 전환, 직업·능력 시너지의 증명, 고유 영역의 경계, Foreshadow Ledger와 Scale Ladder를 관리한다. 강한 적의 숫자만 높이는 가짜 스케일업과 회수되지 않는 장기 복선을 차단한다.

### 7. Continuity Editor

설정, 시간선, 인물 동기, 시점, 호칭, 공개 정보의 일관성을 검사한다. 표면 문장보다 인과관계와 독자에게 알려진 정보 순서를 우선한다.

### 8. Serial Operations Analyst

비축분, 연재 주기, 업로드 메타데이터, 댓글·지표, 이탈 가설, 작가 과부하·고립 신호를 관리한다. 한 주의 변동이나 소수 댓글을 전체 독자 의사로 과잉 해석하지 않는다.

### 9. Incident Diagnoser

실패 trace를 읽고 복수 원인 가설, 근거, 신뢰도, 최소 수정안을 제시한다. 수정은 승인 전 적용하지 않는다.

### 10. Rights & Contract Reviewer

저작권·계약 체크리스트를 제공하고 표준계약서와 비교할 항목을 정리한다. 법률 결론을 확정하지 않으며 고위험 조항은 전문가 상담으로 넘긴다.

## Agent registry and sample loop evaluation

Registered roles are fixed in `config/agent_registry.json`. The current system has 13 roles. Only the Codex runtime agent at `.codex/agents/webnovel-orchestrator.md` owns runtime routing. `prompts/orchestrator.md` is an export adapter and must not be treated as a second independent router.

Intent routing is a deterministic package contract in `config/intent_routes.json`. Run `python scripts/route_intent.py <intent>` before selecting the current workflow phase or specialist role; `.codex/skills/webnovel-production-workflow/SKILL.md` must stay synchronized with this mapping.

When using samples to improve or evaluate the system, use `config/agent_sample_evaluation_policy.json`. Roles 1-9 are included in sample-loop evaluation. Role 10 and context-compounding roles 11-13 are excluded because they use rights, provenance, state, review, and control gates rather than style fidelity scores.

## Context-Compounding Production Loop

Use `config/context_compounding_policy.json` for non-trivial drafting and system improvement.

```text
Inner: classify -> context plan -> evidence pack -> state check -> structured roleplay -> at most two writer candidates -> QA -> review packet
Outer: explicit draft/final pair -> semantic classification -> three cause hypotheses -> same-scope recurrence -> change proposal
Control: candidate approval -> offline replay -> one canary task -> promotion approval -> promote or rollback
```

- Story Bible, approved decisions, character state, and relationship state are canonical. Retrieval summaries are evidence only.
- Missing, stale, or conflicted required evidence blocks drafting.
- Roleplay records knowledge, desire, concealment, expected action, speech purpose, and emotion transition; it is not prose.
- Writer candidates are never merged paragraph by paragraph.
- Episode Memory Delta requires Continuity PASS and explicit human approval before commit.
- Review learning requires distinct draft and approved-final paths. Inspect the latest ten completed reviews and require three matches of classification and scope.
- Every proposed system change requires human candidate approval, replay, one canary task, and separate promotion approval. Automatic promotion is prohibited.

### Collected data authority and migration

- `projects/sample_independent_loops/context_compounding_migration.json` is the current overlay for previously collected sample runs, 100-task ledgers, evaluations, candidates, summaries, and rule records.
- Historical JSONL, evaluation versions, candidate manuscripts, and rule packs remain immutable evidence. They do not become active policy merely because a later system validates them.
- Sample calibration and element packs are derived evidence, not Story Bible facts or durable memory.
- The original four sample TXT files remain unavailable to the active runner. Original-reference scoring stays blocked; earlier derived reports may support bounded hypotheses and fixtures only.
- All twelve recorded improvement candidates have a current resolution in `config/legacy_data_migration_policy.json`.
- Legacy batch runners are read-only by default. Current system changes must use Review Diff recurrence, Change Proposal, approval, Offline Replay, one canary, promotion approval, and rollback.

Run the alignment checks after changing prompts, policies, templates, or collected-data overlays:

```powershell
python scripts/migrate_legacy_context_data.py --project-root ..
python scripts/audit_current_system_alignment.py --project-root ..
```

The sample loop is not a four-sample integration target. It runs four independent sample jobs in parallel. Each TXT follows:

```text
element extraction -> agent recreation -> original-reference evaluation excluding plagiarism checks -> queue improvement point -> close task
```

When a sample original contains enough serial material, do not restart the whole workflow for every later part. Keep the overall cycle at stage 1 and process the original in progressive 10-episode source windows. Use `config/source_chunk_policy.json` and `templates/source_chunk_cycle.json`.

```text
1-10화 테스트 -> 개선/검증 -> 11-20화 테스트 -> 개선/검증 -> 21-30화 테스트 -> ... -> 후반부 window까지 carryover 검증
```

Each 10-episode window must carry forward canon facts, unresolved threads, foreshadow seeds, relationship changes, progression changes, and open questions. The next window starts only after the current window is `verified` or explicitly `blocked_with_evidence`.

Only after all four sample jobs finish should the system compare their results to identify common system weaknesses.

System improvements are not repeatedly applied inside the same task. Each task queues a system-level improvement point, then closes. Between tasks, the system update gate loads the improvement list, deduplicates repeated root causes, applies at most three minimal system changes, and records how the next task must verify them. Use `config/system_improvement_policy.json` and `templates/system_improvement_point.json` for this process.

Sample-loop evaluation must run in this order:

1. Create one independent job for each sample TXT.
2. Extract reusable elements from that one original only.
3. Let the selected agent recreate from the extracted element pack.
4. If the source has serial length, evaluate first against episodes 1-10 of that same original, then advance to 11-20 only after the current window closes.
5. Select the first highest-severity blocking failure for that sample job.
6. Queue one improvement point using `templates/system_improvement_point.json`.
7. Close the task without repeatedly patching the same task.
8. Run the between-task system update gate.
9. Start the next 10-episode window with the improved system and verify the queued point.
10. Record before/after, selected failure, minimal change, next-window carryover, and verification using `templates/agent_sample_loop_evaluation.json` and `templates/source_chunk_cycle.json`.

After package or workflow changes, run:

```powershell
python scripts/audit_agent_registry.py --project-root ..
```

## Workflow

### Step 0 - Prerequisite discovery

- 사용자의 목표, 시간, 장르 후보, 금지선, 기존 자산을 확인한다.
- 필요한 정보와 있으면 좋은 정보를 분리한다.
- 첫 작품의 기본 목표는 사용자가 달리 정하지 않는 한 `완결 가능한 연재 시스템 구축`으로 둔다.

**Gate G0:** 장르 가설, 목표 독자, 작품 약속, 주간 가용 시간이 기록되어야 한다.

### Step 1 - Refresh market evidence

- 목표 플랫폼의 공식 고객센터·공지·공모전 페이지를 우선 확인한다.
- 현재 랭킹 또는 추천면에서 제목 구조, 키워드, 소개문 길이를 표본화한다.
- 플랫폼별 사실, 관찰, 추론을 별도 필드로 저장한다.
- 30일을 넘긴 플랫폼 규칙은 자동으로 `stale` 처리한다.

플랫폼 예시는 고정 진리가 아니다. 현재 확인 가능한 공식 구조상 네이버는 챌린지리그에서 베스트리그로의 승격과 시리즈에디션 기회가 있고, 문피아는 자유 등록과 연재 등급·자체 유료화 경로가 비교적 명확하다. 카카오·조아라는 공개 정보 범위가 더 제한적이므로 추천 직전 재확인이 필수다.

### Step 2 - Lock source of truth

다음 문서를 생성하고 작가 승인을 받는다.

- 한 줄 콘셉트
- 장르와 독자
- 작품 약속
- 결말 방향
- 캐릭터 시트와 결점의 행동 결과
- 핵심 관계 지도와 취약성 공개 계획
- 세계 규칙과 예외
- 주인공의 현재 상황·목적·이유·장애물
- 서사 강도 정책과 고위험 장치 정책
- 금지선
- `story_bible_version`

**Gate G1:** 결말 방향과 작품 약속이 비어 있으면 20화 계획으로 진행하지 않는다.

### Step 3 - Build the serial plan

- Opening Contract, Protagonist Advantage Map, POV·묘사 계약, Exposition Policy를 확정한다.
- 1~5 / 5~25 / 25~100 / 100+ Phase Map을 만들고 Foreshadow Ledger와 Scale Ladder를 생성한다.

- 10개의 아이디어가 아니라 이미 선택된 콘셉트에서 2~3개의 구조안을 만든다.
- 플롯보다 Story를 먼저 잠근다. 결핍, 욕구, 약점, 끝의 변화가 없으면 사건 나열로 넘어가지 않는다.
- 전체 서사를 지탱할 핵심 사건 3개를 잡고, 사건 사이를 관계 변화, 능력 증명, 감정 변주, 무대 확장으로 채운다.
- 20화 사건표와 강도 곡선을 작성한다.
- 3개 이상의 고강도 회차가 연속되지 않도록 회복·관계 회차를 배치한다.
- 감정 고점마다 행동·손실·망설임·선택 중 최소 두 개의 징검다리를 연결한다.
- 1~3화는 갈등, 캐릭터 매력, 작품 약속, 다음 화 이유를 우선한다.
- 4~10화는 독자가 반복 재미를 이해하고 습관화할 구간으로 설계한다.
- 11~20화는 첫 중간 보상과 더 큰 문제의 확장을 포함한다.
- 각 화는 하나의 핵심 포인트를 갖고 끝에 미해결 질문을 남긴다.
- 무대 이동 회차에는 기존 관계를 이어주는 인물·연락·목표 중 하나를 남긴다.
- 주요 캐릭터의 죽음은 인물 서사 완결, 관계 축적, 이후 보상, 작가 승인이 모두 있을 때만 계획한다.

**Gate G2:** 20화 계획, 1~3화 후킹, 화별 클리프행어, 설정 충돌 검사가 통과해야 한다.

### Step 4 - Build buffer

- 최소 출시 버퍼, 권장 버퍼, 깊은 버퍼를 분리하고 독자 반응 확인 주기를 정한다.
- 반응 없이도 쓸 수 있는 기간과 작가의 내적 품질 기록 방식을 운영 계획에 포함한다.

- 승인된 회차 계획에서 장면 목록을 만든다.
- 샘플 스타일 프로필이 있으면 `templates/style_profile.json` 형식으로 검토된 active 규칙만 사용한다.
- 원고 작성 전에 `templates/scene_contract.json` 형식의 회차 계약을 만든다: 핵심 캐릭터 욕망, 주인공이 시작한 선택, 해결할 질문, 상태 변화, 기대·반전, 축적된 독자 보상, 관계 변화, 완급 기능, 다음 화의 구체적 질문, 정보 채널을 고정한다.
- 각 장면은 목표, 장애, 판단, 행동, 결과, 다음 압력, 캐릭터 공개, 전진 축, 설정 정보의 발생 계기와 즉시 사용, 채널별 기능, 마이크로 비트, 금지 동작을 가진다.
- `python scripts/audit_engagement_contract.py <scene-contract.json> --story-bible <story-bible.json>`가 실패하면 초고로 넘어가지 않는다.
- 초안 -> 구조 편집 -> 몰입·감정 감사 -> 문장 편집 -> 연속성 검사의 순서를 지킨다.
- 감정 장면은 초고 직후 확정하지 않고 시간 간격을 둔 전체 흐름 재독을 거친다.
- 1~3화는 주인공의 상황, 목적, 선택 근거를 독백·대화·행동으로 명확히 전달한다.
- 작가의 지속 가능한 속도를 기준으로 목표 버퍼를 설정한다.
- 기본 제안은 주 5회 연재, 출시 전 10화 안팎의 비축분이지만 공식 규정이 아니라 조정 가능한 운영 기준으로 취급한다.
- 버퍼가 목표치보다 낮으면 연재 시작일 또는 주기를 재계산한다.
- 초고는 승인된 정본 안에서 무정지 작성한다. 문장 완성도를 이유로 멈추지 말고, 문장 조립·삭제·압축은 후속 검증 루프에서 처리한다.
- 장면 작성 시 `독백 -> 감각적 동적 묘사 -> 정보 은닉/질문` 순서로 최소 문장 블록을 조립한다.
- 원고 파일이 있으면 `audit_style_profile.py`로 문단 리듬, 정보 채널 다양성, 화말 열린 고리를 감사하고, 결과를 `templates/chapter_audit.json` 형식으로 기록한다.

### Step 5 - Prelaunch verification

출시 전 다음을 검증한다.

- 20화 사건표 존재
- 1~3화에 작품 약속이 실제 장면으로 제시됨
- 각 화 끝에 다음 화를 읽을 이유가 있음
- 샘플 스타일을 적용한 원고는 원문 문장 복제가 아니라 문단 리듬, 정보 채널, 기대-반전-보상, 도전 루프를 기능적으로 재현함
- 차원이동 생존 원정물은 결핍, 시간 압력, 적재 제한, 자원 선택, 귀환 후 재가공, 새 병목이 회차 단위로 연결됨
- 초월자 갤러리형 탑 등반물은 복수 멘토 조언, 주인공의 선택·변형, 증거 기반 사후 분석, 한 번뿐인 공략의 준비 근거가 보임
- 권속 경영형 착각 코미디는 외부 오해의 증거, 주인공의 전략적 결정, 권속별 차별화, 자원/쿨타임 비용, 외부 시점의 다음 사건 생성이 보임
- 1화에서 주인공의 현재 상황과 목적을 이해할 수 있음
- 강도 곡선에 회복·관계 구간이 존재함
- 감정 고점에 필요한 징검다리가 존재함
- 무대 이동이 핵심 관계를 전부 끊지 않음
- 주요 인물 죽음 또는 핵심 관계 단절이 승인 없이 포함되지 않음
- 메타데이터 패키지 완성
- 표절·2차 창작·실존 인물·민감 소재 점검
- 비축분과 연재 캘린더 일치
- 공식 플랫폼 규칙의 최신성

**Gate G3:** 오류 0건, 고위험 경고 0건, 작가 승인 후에만 `ready_for_launch`로 전환한다.

### Step 6 - Platform packaging

같은 작품이라도 플랫폼마다 다음 요소를 별도 버전으로 만든다.

- 제목
- 한줄소개
- 긴소개
- 핵심·보조·주의 태그
- 첫 화 도입부
- 공지
- 업로드 주기

플랫폼의 비공개 추천 가중치를 사실처럼 단정하지 않는다. 제목과 태그 패턴은 현재 표본에서 도출한 가설로 표시한다.

### Step 7 - Serialize and observe

각 회차 게시 시 다음을 기록한다.

- 게시 시각과 플랫폼
- 회차 버전
- 조회·선호·댓글·후원 등 확보 가능한 지표
- 댓글 분류: 칭찬 / 혼란 / 비판 / 요청 / 악성
- 비축분 변화
- 작가 피로도와 연락·고립 위험

원고 방향을 한두 댓글에 즉시 맞추지 않는다. 최소한 반복 신호, 이탈 구간, 작품 약속 미충족 여부를 함께 본다.

### Step 8 - Self-repair loop

운영 실패는 다음 순서로 처리한다.

```text
Bad Trace
-> Diagnose multiple hypotheses
-> Identify minimal responsible scope
-> Propose patch and expected effect
-> Human approval
-> Replay original failing input
-> Compare trace, quality, cost, latency
-> Run full regression suite
-> Lock failure as a new regression case
-> Promote version
```

#### Trace

모든 주요 작업에서 다음을 기록한다.

- project/version/story bible version
- user input and source hashes
- model, prompt version, parameters
- tool calls and retrieved sources
- output hash
- deterministic validation results
- LLM evaluation results
- latency and cost
- human approvals

#### Diagnose

단일 원인으로 단정하지 않고 최소 3개의 가설을 우선순위화한다.

예: "검색 자료를 답변이 무시함"

1. 검색 결과 자체가 부적절했다.
2. context 조립 과정에서 결과가 잘렸다.
3. 상위 프롬프트가 근거 사용보다 문체를 우선시했다.
4. 후속 단계에서 source IDs가 유실됐다.

각 가설에는 근거 span, 반증 조건, 신뢰도를 붙인다.

#### Patch

- 가능한 가장 좁은 범위를 고친다.
- 정본 변경과 실행 로직 변경을 분리한다.
- 프롬프트 전체 재작성보다 데이터 흐름·스키마·검증 누락을 먼저 확인한다.
- 고위험 수정은 자동 적용하지 않는다.

#### Replay

- 원래 실패 입력과 동일한 정본 버전을 사용한다.
- 비결정적 생성은 중요도에 따라 3회 이상 반복한다.
- 단일 성공을 해결로 간주하지 않는다.

#### Regression lock

회귀 사례에는 다음을 저장한다.

- 실패 입력
- 당시 정본·프롬프트·모델 버전
- 실패 유형
- 기대 조건
- 금지 조건
- 수정 diff
- 재실행 결과
- 재발 시 복구 절차

### Step 9 - Weekly review

주간 회고는 `유지 / 수정 / 폐기 / 관찰 지속` 네 칸으로 작성한다.

- 조회수 절대값보다 회차 간 변화와 이탈 지점을 본다.
- 댓글 수가 적으면 정성 신호의 불확실성을 명시한다.
- 버퍼가 5화 아래로 내려가면 감속·휴재·주기 변경안을 계산한다.
- 작가 과부하가 임계치를 넘거나 고립 위험이 있으면 신규 작업보다 휴식·소통·일정 조정을 우선한다.
- 연속 고강도 회차 뒤 독자 피로 신호가 나타나면 자극 강화가 아니라 회복·관계 회차를 검토한다.
- 캐릭터나 결말을 바꾸는 제안은 자동 반영하지 않는다.

### Step 10 - Monetization and contract gate

계약서 또는 유료화 제안이 들어오면 다음을 표로 정리한다.

- 권리 범위
- 독점·선독점·비독점
- 기간과 지역
- 정산 기준, 공제, 주기
- 제목·표지·원고 수정권
- 2차적저작물 권리와 수익 배분
- 해지 조건과 권리 환원
- 보증·면책
- AI 사용 고지나 진정성 관련 조항

**Gate G4:** 계약 체결, 권리 양도, 법률적 안전 판정은 사람과 필요한 경우 전문가가 결정한다.

### Step 11 - Season close and reuse

- 완결 또는 시즌 종료 후 성공·실패 패턴을 정리한다.
- 작품 고유 설정은 다음 프로젝트에 재사용하지 않는다.
- 검증 규칙, 작업 순서, 실패 복구법만 일반화해 스킬 버전을 올린다.

## Narrative design protocol

### 0. Story before Plot

- 사건 배열 전에 주인공의 결핍, 욕구, 약점, 내면 변화 방향을 정의한다.
- 플롯은 Story를 증명하는 외부 사건의 인과 배열이어야 한다.
- 사건이 멋있어도 인물의 내면 변화와 연결되지 않으면 rough idea로 보류한다.

### 1. 강약 곡선

- 강도 4~5 회차는 payoff 또는 중대한 pressure로 제한한다.
- 기본 정책상 고강도는 최대 2회 연속이며, 이후 3화 이내에 recovery 또는 relationship 회차를 둔다.
- 가벼운 회차에도 작은 목표, 관계 변화, 정보 변화 중 하나는 반드시 존재한다.
- 강도를 낮춘다는 이유로 작품 약속을 중단하지 않는다. 반복 재미는 낮은 강도에서도 다른 형태로 제공한다.

### 2. 감정 징검다리

감정 고점 전에는 다음 중 최소 두 개를 이전 또는 현재 회차에 배치한다.

1. 인물이 소중히 여기는 대상·신념의 행동 증명
2. 작은 손해나 위험을 먼저 감수한 기록
3. 두려움·망설임·회피의 노출
4. 선택지가 줄어드는 외부 압력
5. 최종 선택 직전의 자발적 결단

작가만 아는 과거 설정은 징검다리로 인정하지 않는다. 독자가 실제로 본 장면만 근거로 계산한다.

### 3. 초반 방향성

1화 종료 시 독자는 다음 질문에 답할 수 있어야 한다.

- 누구의 이야기인가
- 지금 어떤 문제에 처했는가
- 당장 무엇을 하려 하는가
- 실패하면 무엇을 잃는가
- 무엇이 그것을 막는가

세계관의 전체 역사나 능력 체계는 이 다섯 질문보다 뒤에 둔다.

### 4. 캐릭터 결점과 유대

- 결점은 실제 선택을 나쁘게 만들거나 관계 비용을 발생시켜야 한다.
- 상처는 행동 패턴, 말버릇, 거리감, 책임 방식 중 하나로 외부화한다.
- 진심 공개는 설명문보다 선행 행동 뒤에 배치한다.
- 핵심 관계마다 `거리 변화`, `신뢰 변화`, `공유 비밀`, `미해결 갈등`을 추적한다.

### 5. 독백과 독자 동지화

- 독백은 정보 전달 목적을 명시한다: 상황 정리 / 위험 평가 / 목표 / 선택 근거 / 타인 평가.
- 같은 기능의 독백을 연속 반복하지 않고 행동, 대화 상대, 상태창, 기록물 등으로 변주한다.
- 주인공의 판단이 독자에게 납득되려면 대안과 비용을 최소한 암시해야 한다.
- 독백은 장면을 대신하지 않고 장면 해석을 돕는다.

### 5-1. 레고 블록형 문장 조립

- 문장 초안은 `독백 기능`, `감각적 동적 묘사`, `호기심 주입` 세 블록으로 조립한다.
- 동사는 감정을 싣는 장치로 사용한다. 일반 동사를 구체 동사로 바꾸되 과장된 장식어를 남발하지 않는다.
- 정보 은닉은 다음 행동을 유도하는 미공개 카드, 소품, 의도, 비용, 정보 격차로 만든다.
- 문장 조립은 속도를 위한 절차이며, 최종 문체는 후처리와 작가 검토에서 정리한다.

### 6. 개연성·주변 피해 감사

선행, 희생, 구조, 복수, 처벌 장면마다 다음을 묻는다.

- 위기의 원인은 누구에게 있는가
- 다른 선택지가 있었는가
- 주변 피해자는 누구인가
- 주인공은 피해를 줄이기 위해 무엇을 했는가
- 책임과 결과가 이후 서사에 남는가

선한 의도만 있고 책임이 삭제된 선택은 `causality_or_collateral_blindness`로 분류한다.

### 7. 무대 이동과 관계 연속성

무대를 옮길 때 다음 중 하나 이상을 유지한다.

- 기존 핵심 동료 동행
- 기존 인물과의 정기 연락
- 이전 무대의 미해결 목표가 새 무대 사건에 영향
- 재회 시점 또는 재회 조건

핵심 관계를 모두 제거하는 전환은 새 작품처럼 느껴질 수 있으므로 사람 승인을 요구한다.

### 8. 캐릭터 죽음 게이트

비중 있는 캐릭터의 죽음은 다음을 모두 충족해야 한다.

- 인물의 가치관과 선택이 완결되는가
- 충분한 관계 축적이 있었는가
- 충격만을 위한 선택이 아닌가
- 생존했을 때 가능한 더 강한 서사를 검토했는가
- 죽음 이후 새로운 정서 보상과 관계 축이 있는가
- 핵심 독자 보상을 철회하지 않는가
- 작가가 명시적으로 승인했는가

### 9. 작가 지속 가능성

- 주간 가용 시간과 연재량을 함께 관리한다.
- 피로가 `critical`이거나 연락 단절 위험이 있으면 출시·증편보다 감속을 우선한다.
- 휴재·감속 공지는 관계 유지의 운영 작업으로 취급한다.
- 집필 문제와 인간관계 문제를 분리하고 최소 소통 계획을 유지한다.


### 10. 1화 전투 감사

- 전투 전에 주인공의 정체·목적·승패 비용이 보이는가.
- 독자가 이해한 카드와 적이 모르는 정보가 있는가.
- 전투가 주인공을 각인하거나 새로운 목적을 만드는가.
- 기술 교환만 남는다면 전투를 이후 화로 옮기거나 aftermath 중심으로 재설계한다.

### 11. 정보 공개 예산

- 현재 장면에서 선택에 영향을 주지 않는 세계 규모 정보는 지연한다.
- 생존·비용·금지 조건은 필요한 순간 바로 공개한다.
- 고유명사와 세력 설명이 캐릭터 행동보다 앞서지 않게 한다.

### 12. 직업·고유 영역 증명

- 직업은 전문 용어가 아니라 관찰·판단·행동 방식으로 드러난다.
- 능력과 직업의 조합이 최소 두 개 이상의 독특한 해결법을 만들어야 한다.
- 고유 영역은 타인이 쉽게 복제할 수 없지만 비용과 경계가 있어야 한다.

### 13. 시점·묘사 운용

- 장면마다 누가 보고 판단하는지 고정한다.
- 시점 전환은 문단·장면·대사·속마음 같은 명시적 앵커를 사용한다.
- 평시는 직접 묘사, 하이라이트는 제한적 간접 묘사로 대비를 만든다.

### 14. 장기 구간 전환

- 1~5화는 주인공을 기억하게 하고, 5~25화는 성장 엔진을 믿게 한다.
- 25~100화는 기존 조연과의 관계를 깊게 하고, 신규 캐릭터 수만 늘리지 않는다.
- 100화 이후에는 더 큰 적뿐 아니라 더 높은 권력자·기관·의사결정 범위를 제공한다.

### 15. 복선 리마인드

- 5~8화 안의 복선은 불필요한 재설명 없이 회수한다.
- 장기 복선은 회수 직전 핵심 대사·이미지·행동을 짧게 재활성화한다.
- 리마인드는 답을 미리 설명하는 것이 아니라 독자가 연결할 기억을 복원하는 기능만 수행한다.

### 16. 반응 독립성

- 댓글·조회는 정해진 리뷰 시점에 묶어서 본다.
- 개별 반응으로 정본이나 결말을 즉시 바꾸지 않는다.
- 버퍼가 충분할수록 반응 노이즈와 마감 압박을 분리할 수 있으므로 깊은 버퍼를 선택지로 유지한다.

### 17. 영상 클립 묘사 훈련

- 100~300초 내외의 검증된 장면을 고르고 15초 단위로 멈춰 행동, 대사, 배경, 표정, 시선, 소품을 즉시 문장화한다.
- 컷 전환은 문단 전환과 문장 길이로, 클로즈업은 손·숨·시선·소품의 세부 묘사로 치환한다.
- 훈련 결과는 표현 데이터베이스로만 사용하고, 원 장면의 고유 설정이나 문장을 복제하지 않는다.

### 18. 작가 색채와 선택적 분석

- 분석 대상은 장르별 1~2개로 제한한다.
- 작가의 본래 톤과 맞는 성공작을 우선하고, 최신 베스트나 현재 노출면 변화에 따라 갱신한다.
- 비판보다 흡수 태도를 우선한다. 흡수 대상은 문장이 아니라 구조, 리듬, 정보 배치, 보상 주기, 독자 약속이다.

### 19. 무정지 초고와 80화 확장

- 전체를 지탱할 핵심 사건 3개를 잡고, 그 사이를 감정 변주, 관계 변화, 능력 증명, 무대 확장으로 채워 중장기 분량을 만든다.
- 아웃라인은 집필을 막지 않는 러프한 수준으로 유지한다.
- 초고는 멈추지 않고 완주하고, 삭제·압축·순서 조정은 검증 루프와 퇴고 단계에서 수행한다.

## Tool/model routing

### 모델이 담당할 영역

- 콘셉트 후보와 비교
- 캐릭터 욕망·갈등 설계
- 장면 대안
- 대사와 문장 초안
- 문장 조립 블록과 무정지 초고
- 독자 반응 가설
- 실패 원인 가설과 수정안

### 스크립트가 담당할 영역

- JSON Schema 검증
- 정본 버전 일치
- 필수 필드와 20화 계획 검사
- 1~3화 hook/cliffhanger 필드 검사
- 버퍼와 연재 일정 계산
- ID 중복, 회차 번호 누락, 상태 전이 오류
- 강도 연속성, 감정 징검다리, 무대 이동 관계 앵커 검사
- 주요 인물 죽음 승인과 작가 지속 가능성 게이트 검사
- 회귀 fixture 실행
- Hyperagent export 생성

### 사람이 승인할 영역

- 콘셉트와 결말 방향
- 정본을 바꾸는 수정
- 최종 원고와 작가 문체
- 핵심 관계 단절과 비중 있는 캐릭터의 죽음
- 과부하 시 연재 감속·휴재 결정
- 출시와 휴재
- 저작권·계약·수익화
- 실제 배포

## Error classification and recovery

### E1 Missing prerequisite

증상: 장르, 작품 약속, 결말 방향이 없음.

복구: 질문 또는 2~3개 가설안을 제시한다. 대량 집필은 중지한다.

### E2 Canon drift

증상: 캐릭터 능력, 세계 규칙, 공개 정보가 정본과 충돌한다.

복구: 충돌 위치를 표시하고 `원고 수정`과 `정본 변경` 두 대안을 분리한다. 정본 변경은 승인 필요.

### E3 Weak opening promise

증상: 1~3화가 배경 설명에 머물고 반복 재미가 보이지 않는다.

복구: 작품 약속을 행동 장면으로 앞당긴 2~3개 구조안을 만든다. 설정 설명을 삭제하기보다 공개 시점을 늦춘다.

### E4 Buffer collapse

증상: 현재 버퍼가 경고선 아래로 내려감.

복구: 주기 감속, 짧은 휴재, 장면 범위 축소, 비핵심 작업 중단을 비교한다. 작가 건강과 완결 가능성을 우선한다.

### E5 Metric decline

증상: 조회·선호·댓글이 하락함.

복구: 발견성, 초반 약속, 회차 만족, 업로드 불규칙, 장르 불일치, 표본 부족을 별도 가설로 진단한다. 한 원인으로 확정하지 않는다.

### E6 External platform change

증상: 규칙·공모전·노출면이 저장된 프로필과 다름.

복구: 공식 자료를 다시 조사하고 프로필 날짜·신뢰도를 갱신한다. 과거 규칙으로 자동 실행하지 않는다.

### E7 Temporary tool failure

증상: 검색, 저장, 모델 호출의 일시 오류.

복구: 지수 백오프로 제한 재시도한다. 동일 오류가 반복되면 대체 경로를 사용하고 trace에 남긴다.

### E8 Legal/IP risk

증상: 무단 2차 창작, 표현 유사성, 광범위한 권리 양도, 불명확한 정산.

복구: 자동 진행을 중단하고 위험 항목과 확인 질문을 생성한다. 안전하다고 보증하지 않는다.

### E9 Intensity saturation

증상: 고강도 사건·감정이 연속되어 대비와 피로 회복 구간이 없다.

복구: 사건을 더 키우지 않는다. 기능이 중복되는 고점을 합치고 recovery/relationship 회차를 삽입하며 낮은 강도에서도 작품 약속을 제공한다.

### E10 Unearned emotional peak

증상: 희생·고백·죽음·화해가 독자에게 갑작스럽거나 감정 강요로 보인다.

복구: 독자가 실제로 본 행동·손실·망설임·선택을 추적한다. 부족한 징검다리를 앞 회차에 분산하고 하이라이트 내부의 설명은 줄인다.

### E11 Protagonist orientation failure

증상: 초반에 주인공의 상황, 목적, 이유, 장애물을 파악하기 어렵다.

복구: 세계관 설명보다 구체 상황과 당장 실행할 목표를 앞당긴다. 1화 안에 방향성을 행동으로 제시한다.

### E12 Reader alignment failure

증상: 주인공의 선택 근거가 보이지 않아 독자가 판단을 공유하지 못한다.

복구: 독백·대화·행동을 통해 위험 평가와 선택 근거를 보완하되 설명 반복을 피한다.

### E13 Character bond gap

증상: 사연은 많지만 행동 축적과 진심 공개가 없어 캐릭터 애착이 형성되지 않는다.

복구: 결점이 만든 선택 비용, 작은 신뢰 행동, 취약성 공개 장면을 순서대로 설계한다.

### E14 Causality or collateral blindness

증상: 주인공의 선행·희생이 주변 피해와 책임을 삭제해 민폐나 무모함으로 보인다.

복구: 원인, 대안, 책임 소재, 피해 완화 노력, 이후 결과를 명시한다.

### E15 Relationship discontinuity

증상: 무대 이동이나 시즌 전환으로 기존 핵심 관계가 동시에 사라진다.

복구: 동행자, 연락, 미해결 목표, 재회 조건 중 하나를 남기고 관계 단절은 승인 대상으로 올린다.

### E16 Author sustainability risk

증상: 버퍼 붕괴와 함께 작가 과부하·고립 위험이 나타난다.

복구: 신규 분량을 강제하지 않는다. 감속·휴재·작업 범위 축소·최소 소통 계획을 먼저 결정한다.

### E17 High-risk character death

증상: 핵심 보상 캐릭터의 죽음이 충격 장치로만 사용되거나 승인·대체 보상 없이 계획된다.

복구: 생존 대안, 인물 서사 완결성, 관계 축적, 이후 정서 보상, 독자 약속 훼손을 비교하고 사람 승인 전 차단한다.


### E18 Opening combat without narrative anchor

1화 전투에 캐릭터 각인, 목적, 승패 비용, 독자가 아는 카드가 없다. 전투를 이동하거나 서사 기능을 먼저 설계한다.

### E19 Exposition overload

현재 선택과 무관한 역사·세력·규칙이 초반 행동보다 앞선다. 즉시 필요한 설정과 지연 설정으로 분리한다.

### E20 Profession-skill disconnect

직업이 명찰에 머물고 능력 사용이나 판단에 영향을 주지 않는다. 전이 가능한 전문성과 증명 장면을 다시 설계한다.

### E21 POV anchor failure

독자가 인식 주체를 잃는 무표지 시점 전환이 발생했다. 장면 경계와 전환 앵커를 명시한다.

### E22 Foreshadow memory gap

장기 복선이 리마인드 없이 회수되어 독자가 연결하기 어렵다. Foreshadow Ledger와 리마인드 장면을 추가한다.

### E23 Unique-domain dilution

주인공의 고유 영역이 비용 없이 복제되거나 모든 인물에게 평준화됐다. 독점 경계와 역할 차이를 복구한다.

### E24 False scale-up

숫자와 적의 힘만 증가하고 접근 권한·인물 격·결정 영향 범위가 상승하지 않았다. Scale Ladder를 재설계한다.

### E25 Reaction-driven canon churn

소수 댓글이나 단기 지표에 따라 정본이 반복 변경된다. 변경을 주간 리뷰와 승인 게이트로 되돌린다.

## Evaluation contract

### 결정적 검사

- JSON Schema 통과
- 프로젝트·정본 버전 일치
- 20개 이상의 회차 계획
- 1~3화 hook과 conflict 존재
- 모든 계획 회차에 cliffhanger 또는 next reason 존재
- ready/serializing 상태의 비축분·메타데이터·IP 검토 통과
- 중복 ID와 회차 번호 누락 없음
- 1화의 주인공 상황·목적·장애물 존재
- 고강도 연속 상한 준수와 회복 회차 존재
- 감정 고점의 최소 징검다리 충족
- 무대 이동의 관계 앵커 존재
- 주요 캐릭터 죽음의 명시적 승인
- 작가 과부하·고립 위험 출시 차단
- 샘플 스타일 적용 원고의 문단 리듬, 정보 채널 다양성, 화말 열린 고리 감사 실행

### 의미 기반 평가

각 항목을 1~5점으로 평가하고 근거 문장을 남긴다.

- 작품 약속의 명확성
- 주인공의 선택과 인과성
- 캐릭터 매력과 agency
- 강약 대비와 독자 피로 관리
- 감정 축적의 충분성
- 주인공 상황·목적의 명확성
- 주인공과 독자의 판단 정렬
- 결점이 선택과 관계에 미치는 실제 영향
- 주변 피해와 책임의 반영
- 관계 연속성
- 설명 부담과 공개 타이밍
- 회차별 보상
- 클리프행어의 정당성
- 정본 일관성
- 플랫폼 포장 적합성
- 문체 일관성
- 장면 추진력
- 정보 전달의 자연스러움
- 기대와 반전의 보상성
- 개그와 긴장의 균형
- 캐릭터 목소리 구분
- 화말 흡인력
- 결핍 명확성
- 시간 압력
- 적재 제한
- 자원 선택의 의미
- 보상 재사용
- 전투의 준비·약점 공략 논리
- 설명의 행동 전환
- 조력자와 주인공의 의사결정 균형
- 차원별 행동 동사 차별성
- 귀환 성과와 다음 병목
- 갤러리 조언의 다중 관점성
- 증거 피드백의 새 정보성
- 멘토 조언을 주인공이 변형하는 정도
- 한 번뿐인 공략의 준비 축적
- NPC와 갤러리의 정서 기능
- 오해의 관찰 근거
- 권속 위임 속 주인공 agency
- 권속 역할과 충성 표현의 차별성
- 혈력·쿨타임·슬롯의 선택 비용
- 외부 시점이 다음 갈등을 만드는 정도

LLM judge 단독 점수로 출시를 승인하지 않는다. 결정적 검사와 작가 검토를 함께 요구한다.

### 변경 검증

- 원래 실패 사례 통과
- 기존 회귀 사례 전부 통과
- 중요 변경은 최소 3회 재실행
- 비용·지연이 설정한 한도를 넘지 않음
- 새로운 정본 충돌이 없음

## Gotchas

- 주 5회, 3,800~5,000자, 10화 버퍼는 운영 기준이지 모든 플랫폼의 공식 규칙이 아니다.
- 현재 인기 제목 패턴을 그대로 복제하지 말고 독자 기대를 표현하는 구조만 추출한다.
- 댓글은 참여 독자의 편향된 표본일 수 있다.
- 조회 하락은 원고 품질 외에도 노출, 일정, 시즌성, 제목·표지 문제일 수 있다.
- LLM의 자연어 평가는 변동한다. 중요 품질은 반복 실행과 사람 검토가 필요하다.
- 계약 비교는 법률 자문을 대체하지 않는다.
- 참고작의 문장·장면·고유 설정을 입력 데이터로 대량 복제하지 않는다.
- 정본 변경을 원고 수정처럼 조용히 처리하지 않는다.
- 회복 회차를 filler로 취급하지 않는다. 관계·매력·작은 목표가 있어야 한다.
- 감정 장면의 세기를 높이기 전에 독자가 본 징검다리 수를 확인한다.
- 메인 관계의 죽음·이별은 조회수용 충격 장치로 자동 제안하지 않는다.
- 작가의 연락 단절을 집중력 전략으로 정당화하지 않는다.

## Validation checklist

### Discovery

- [ ] 목표와 완료 기준이 명확하다.
- [ ] 주간 가용 시간과 지속 가능한 연재 속도가 기록됐다.
- [ ] 금지 소재와 법적 위험이 확인됐다.

### Planning

- [ ] 한 줄 콘셉트와 작품 약속이 있다.
- [ ] 결말 방향을 안다.
- [ ] 캐릭터 욕망과 세계 규칙이 행동 갈등으로 연결된다.
- [ ] 주인공의 현재 상황·목적·이유·장애물이 명확하다.
- [ ] 결점이 선택 비용과 관계 변화로 이어진다.
- [ ] 핵심 관계 지도와 취약성 공개 계획이 있다.
- [ ] 20화 사건표와 각 화의 끝 질문이 있다.
- [ ] 주인공의 직업·능력 시너지와 고유 영역의 경계가 있다.
- [ ] POV·묘사·정보 공개 정책과 장기 Phase Map이 있다.
- [ ] Foreshadow Ledger와 Scale Ladder의 초기 항목이 있다.

### Buffer

- [ ] 1~3화에 갈등·매력·궁금증이 있다.
- [ ] 1화에 주인공의 상황과 목적이 드러난다.
- [ ] 강도 곡선에 recovery/relationship 회차가 있다.
- [ ] 감정 고점마다 독자가 본 징검다리가 있다.
- [ ] 독백·대화가 선택 근거를 전달하되 설명을 반복하지 않는다.
- [ ] 샘플 스타일 프로필을 쓴 경우 회차 계약과 장면 비트가 먼저 작성됐다.
- [ ] `audit_style_profile.py` 결과의 경고를 검토하고 의도적 예외를 기록했다.
- [ ] 차원이동 생존 원정물은 차원 계약, 인벤토리 상태, 장비 의존성, 포기한 자원 목록을 갱신했다.
- [ ] 초월자 갤러리형 탑 등반물은 멘토 지식 상태, 조언 충돌, 층계 기록, 업로드 피드백을 갱신했다.
- [ ] 권속 경영형 착각 코미디는 권속 등록부, 혈력 경제, 평판 믿음 상태, 숨은 정체 상태를 갱신했다.
- [ ] 원고와 정본 버전이 일치한다.
- [ ] 목표 비축분과 캘린더가 맞는다.
- [ ] 1화 전투가 있다면 목적·비용·reader-known card가 있다.
- [ ] 1~25화에 직업·능력·고유 영역 증명 장면이 있다.
- [ ] 8화를 넘는 복선에 리마인드 계획이 있다.
- [ ] 장면 시점 전환에 명확한 앵커가 있다.

### Launch

- [ ] 제목·소개·태그·연령등급·공지 준비가 끝났다.
- [ ] 플랫폼 규칙을 최근 공식 자료로 확인했다.
- [ ] 교정·몰입·감정·연속성·IP 점검을 통과했다.
- [ ] 무대 이동과 핵심 관계 단절 위험을 검토했다.
- [ ] 주요 캐릭터 죽음이 승인 없이 포함되지 않았다.
- [ ] 작가가 최종 원고를 직접 검토했다.

### Operation

- [ ] 지표와 댓글을 분리해 기록한다.
- [ ] 버퍼 경고선과 휴재 기준이 있다.
- [ ] 작가 과부하·고립 위험과 최소 소통 계획을 확인한다.
- [ ] 댓글·지표 확인 주기와 정본 변경 지연 규칙을 지킨다.
- [ ] 장기 구간의 관계·스케일 단계가 실제로 상승하고 있는지 검토한다.
- [ ] 모든 실패에 trace와 분류가 있다.
- [ ] 수정 후 원래 실패 입력과 전체 회귀를 실행했다.

### Monetization

- [ ] 권리 범위와 독점 여부를 확인했다.
- [ ] 정산식과 공제 항목을 확인했다.
- [ ] 2차 사업, 해지, 권리 환원을 확인했다.
- [ ] 필요한 경우 전문가 검토를 받았다.

## Bundled scripts

- `scripts/validate_project.py`: 프로젝트의 결정적 출시 조건 검사
- `scripts/audit_narrative.py`: 전투·정보량·직업 시너지·복선·고유 영역·스케일을 결정적으로 감사
- `scripts/audit_lexicon.py`: 웹소설 용어 사전, 금칙어, AI-tell 문구, 캐릭터 보이스 템플릿을 검증하고 원고 내 위험 표현을 감사
- `scripts/audit_style_profile.py`: 원고의 문단 리듬, 정보 채널 다양성, 화말 열린 고리를 샘플 스타일 프로필 기준으로 감사
- `scripts/audit_engagement_contract.py`: 캐릭터 주도 선택, 화 단위 상태 변화, 장면 전진 축, 설정의 즉시 사용, 다음 화의 구체적 질문을 결정적으로 감사
- `scripts/run_semantic_rubric.py`: 사람 또는 별도 judge가 작성한 1~5 의미 루브릭 점수를 정책 기준으로 검증
- `scripts/run_semantic_rubric_tests.py`: 의미 점수마다 장면·산출물 근거가 존재하는지 정상·실패 경로를 회귀 테스트
- `scripts/audit_workspace_projects.py`: `projects/project_registry.json`에 따라 현재 프로젝트와 과거 회차 묶음을 분리하고 현재 프로젝트만 정식 게이트로 검증
- `scripts/run_portable_export_tests.py`: 단일 JSON을 임시 환경에 복원해 config/schema/template 의존 스크립트를 실제로 실행
- `scripts/calibrate_from_samples.py`: 사용자가 제공한 TXT/MD 샘플에서 원문 복사 없이 용어, 말투, 문단 구조, AI-tell 대조 후보를 추출
- `scripts/run_regression.py`: 정상·실패 fixture 및 누적 회귀 사례 실행
- `scripts/build_export.py`: Markdown 원본과 scripts를 단일 Hyperagent 스타일 JSON으로 빌드

## Lexicon layer

Use `lexicons/*.json` when drafting, rewriting, metadata generation, or sample analysis needs vocabulary control.

- `webnovel_terms.ko.json`, `genre_terms.ko.json`, and `platform_keywords.ko.json` are starter dictionaries. Keep entries marked `pending_sample_calibration` until the user supplies current popular webnovel TXT samples.
- `sample_group_01_terms.ko.json` and `sample_group_01_voice.ko.json` contain reviewed candidates derived from the supplied group_01 samples. Prefer entries marked `active`; treat `candidate` entries as human-review evidence, not hard rules.
- `ai_tell_phrases.ko.json` and `prohibited_phrases.ko.json` are seeded from the local `im-not-ai` taxonomy. Treat S1 hits as blockers unless they are protected quotes, proper nouns, numeric facts, or explicit in-world terms.
- `character_voice.template.json` is not a finished voice profile. Fill it from character-specific dialogue and monologue samples before enforcing voice drift.
- Run `python scripts/audit_lexicon.py` after editing dictionary files. Run `python scripts/audit_lexicon.py --manuscript <path>` before calling a Korean manuscript clean enough for final guard review.
- When the user provides current popular webnovel TXT/MD samples, run `python scripts/calibrate_from_samples.py <sample-dir> --output <report.json> --path-mode basename` first. Use the report as candidate evidence only; do not promote a new rule unless it is sample-backed and reviewed.
- Read `reports/group_01_im_not_ai_alignment.json` before changing AI-tell thresholds. General grammar patterns are density warnings; explicit AI/meta-summary phrases remain strict blockers.

## Sample style layer

Use `SAMPLE_STYLE_PROTOCOL.md` and `templates/style_profile.json` when the user supplies reference samples or asks to transplant a sample's webnovel feel.

- Run `calibrate_from_samples.py` first to derive portable candidates: term counts, endings, line-structure metrics, and phrase-rule collisions.
- Promote only reviewed candidates into a style profile. The profile stores derived structure, not source prose.
- Before drafting, create a scene contract from `templates/scene_contract.json`.
- After drafting, run `python scripts/audit_style_profile.py <manuscript> --profile <style_profile.json>` when a manuscript file exists.
- If the result is `WARN`, decide whether the warning is an intentional scene-mode exception or a revision target.
- For 1~5 scoring, store reviewer or judge scores and evidence by dimension in the `templates/chapter_audit.json` shape and validate them with `run_semantic_rubric.py`. The rubric includes the ten engagement dimensions and readability delivery gate from `ENGAGEMENT_CHARACTER_SYSTEM.md`.
- Style-profile warnings do not replace `$humanize-korean`, its path-and-SHA-256-bound completion report, `audit_lexicon.py --manuscript`, or `ai_tell_guard.py --fail-on-s1`.

## Dimension survival layer

Use this layer when the concept includes dimension travel, expedition farming, base growth, equipment dependencies, timed return, or survival logistics.

- Read `references/dimension-survival/survival-expedition-loop.md` before planning the season engine.
- Read `references/dimension-survival/resource-choice-and-conversion.md` before writing farming or loot scenes.
- Read `references/dimension-survival/procedural-exposition.md` before introducing a new dimension, technology, system rule, or expert explanation.
- Read `references/dimension-survival/utility-to-trust-relationship.md` before adding a technical companion or survival partnership.
- Read `references/styles/dimension-survival-expedition.md` before drafting prose in this mode.
- Use `templates/dimension_contract.json`, `inventory_state.json`, and `equipment_dependency.json` to track continuity when named gear, revisitable dimensions, or resource dependencies appear.
- Do not merge this style with fast retry/community-comment samples. Shared webnovel principles may be reused, but this engine's core loop is expedition, choice, return, and conversion.

## Transcendent gallery layer

Use this layer when the concept includes tower climbing, transcendent community mentors, uploaded combat evidence, one-life progression, or gallery-as-emotional-chorus.

- Read `references/transcendent-gallery/distributed-mentor-feedback.md` before using community advice as a growth mechanism.
- Read `references/transcendent-gallery/evidence-based-combat-review.md` before writing post-combat uploads or video review comments.
- Read `references/transcendent-gallery/one-life-tower-progression.md` before planning major stage clears.
- Read `references/transcendent-gallery/gallery-emotional-chorus.md` before making the community emotionally important.
- Read `references/styles/transcendent-gallery-climb.md` before drafting prose in this mode.
- Use `templates/mentor_knowledge_state.json` and `stage_history.json` to track mentor specialties, advice conflicts, uploaded evidence, and stage lessons.
- Do not merge this with retry-loop community samples. This engine uses advice before and after a one-life clear, not information carried across deaths.

## Vampire retainer layer

Use this layer when the concept includes retainers, delegated combat, vampire/domestic comedy, evidence-based misunderstanding, hidden identity, or reputation inflation.

- Read `references/vampire-retainer/evidence-based-misunderstanding.md` before writing outside overestimation.
- Read `references/vampire-retainer/delegated-combat-and-agency.md` before letting retainers fight in the protagonist's place.
- Read `references/vampire-retainer/retainer-growth-economy.md` before adding new retainers, blessings, blood resources, cooldowns, or territory.
- Read `references/vampire-retainer/supernatural-domestic-comedy.md` before using vampire constraints or forced noble speech as comedy.
- Read `references/styles/vampire-retainer-misunderstanding.md` before drafting prose in this mode.
- Use `templates/retainer_registry.json`, `reputation_belief_state.json`, and `hidden_identity_state.json` to track retainer roles, public beliefs, rumors, and dual-identity risk.
- Do not let retainers remove protagonist agency. The protagonist must still choose targets, assignments, investments, and reputation responses.

## Manuscript Length Gate

Each episode TXT is incomplete until it reaches at least 3600 non-space characters. Count length by removing all Unicode whitespace, then counting the remaining characters. Run:

```powershell
python scripts/audit_episode_length.py <episode-path> --min-nonspace 3600
```

`EPISODE_NONSPACE_UNDER_MINIMUM` is a blocking failure for candidate and final manuscript status.

## Non-goals

- 작가의 최종 창작 의사결정을 대체하지 않는다.
- 자동으로 플랫폼에 게시하거나 계약에 동의하지 않는다.
- 특정 플랫폼의 비공개 알고리즘을 안다고 주장하지 않는다.
- 한 번의 성공 재실행을 완전한 복구로 간주하지 않는다.

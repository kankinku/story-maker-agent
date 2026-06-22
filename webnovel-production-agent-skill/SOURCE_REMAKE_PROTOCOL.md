# Source Remake Isolation Protocol

원본 기반 리메이크는 원문을 집필 프롬프트에 직접 넣어 문장을 변형하는 작업이 아니다. 원문 분석과 새 작품 집필을 서로 격리한다.

## Required pipeline

1. `source lock`: 원본 경로와 SHA-256을 기록하고 읽기 전용 근거로 고정한다.
2. `extract`: 원본에서 세계 규칙, 주인공, 핵심 캐릭터, 능력·비용, 관계, 장르 엔진, 작품 약속, 장기 갈등만 구조화한다.
3. `abstract`: 원문 문장, 대사, 장면 순서, 농담, 회차 분할을 제거하고 재사용 가능한 설정·기능으로 추상화한다.
4. `canon approval`: 추출 결과를 `templates/source_remake_blueprint.json`에 저장하고 사람이 유지·변경·폐기 항목을 승인한다.
5. `rebuild`: 승인된 블루프린트에서 새 Story Bible, 새 장기 방향, 새 20화 계획과 회차 계약을 만든다.
6. `draft`: 집필자는 블루프린트, Story Bible, 회차 계획, 회차 계약만 사용해 새 원고를 쓴다.
7. `compare`: 별도 평가 단계가 원문과 새 원고를 다시 열어 설정 보존, 표면 복사, 사건 배열 복제를 검사한다.
8. `improve`: 비교 결과의 첫 최고 심각도 실패만 수정한 뒤 같은 검사를 반복한다.

## Input isolation

집필 프롬프트와 Writer Context에는 다음을 넣지 않는다.

- 원본 TXT/MD/PDF 본문
- 원본 장문 발췌
- 원본 대사 목록
- 원본 장면을 순서대로 요약한 재현용 시놉시스
- 원본 회차를 문장 단위로 바꿔 쓰라는 지시

허용되는 Writer 입력은 다음뿐이다.

- 승인된 `source_remake_blueprint.json`
- 그 블루프린트에서 만든 Story Bible
- 새 작품의 episode plan과 engagement contract
- 현재 캐릭터·관계 상태와 승인된 변경 이력

원본 경로와 해시는 provenance 용도로 기록할 수 있지만 원문 내용은 Writer에게 전달하지 않는다.

## Extraction contract

블루프린트는 최소한 다음을 포함한다.

- 주인공의 정체, 욕망, 결핍, 능력, 비용, 선택 습관
- 핵심 캐릭터별 기능, 욕망, 주인공과의 관계
- 세계 규칙, 예외, 비용, 이해관계
- 반복 재미를 만드는 core loop와 reward loop
- 반드시 보존할 설정과 새로 설계할 영역
- 표면 복사를 막는 금지 목록
- 원본과 다른 새 시즌 방향 및 첫 아크 종료 상태

## Completion gates

- 블루프린트가 승인되기 전에는 회차 원고를 쓰지 않는다.
- Writer Context에 원문 본문이 포함되면 `RAW_SOURCE_IN_WRITER_CONTEXT`로 중단한다.
- 새 원고가 원본 사건 순서를 그대로 따라가면 리메이크가 아니라 축약·리마스터로 분류한다.
- 비교 단계는 설정 보존과 표면 비복제를 별도 판정한다.
- 이후 `$humanize-korean`, lexicon, AI-tell guard 순서는 기존 원고 게이트를 따른다.

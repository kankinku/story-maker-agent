# WebNovel Production Loop 결함 해결 보고서

- 완료 버전: `1.14.0`
- repair loop: 8회
- 시스템 판정: **PASS**

## 해결된 항목

- canon delta silent drop을 `CANON_TARGET_UNSUPPORTED`로 차단했다.
- 9개 intent의 단계·루프·담당 역할을 `intent_routes.json`과 `route_intent.py`로 결정화했다.
- Review Packet과 Replay가 실제 파일 없이는 통과하지 못하도록 했다.
- 동일 Review ID 복제, 중복 Evidence ID, 중복 캐릭터·관계·참여자 ID를 차단했다.
- 다른 캐릭터의 비밀을 정본 지식 근거 없이 사용하는 역할극을 차단했다.
- state commit 시 `last_evidence`를 episode/source ID로 갱신한다.
- commit과 component version 전이에 JSON schema 검증을 추가했다.
- replay/canary 회귀 증거 없는 rollback을 차단했다.
- workflow state에 Context/State/Review/Proposal/Registry/Approval/Canary 필드를 추가하고 terminal state 재변경을 차단했다.
- project에 `context_compounding`, output에 evidence/version/uncertainty/approval을 필수화했다.
- `--humanized` flag만으로는 완료되지 않으며 manuscript path와 SHA-256이 일치하는 humanization report를 요구한다.
- Windows UTF-8 BOM 입력과 한국어 PowerShell 검사 절차를 표준화했다.
- legacy sample의 원본 존재 여부를 `source_availability`로 분리하고 Story Bible 부재를 `null`로 표현한다.
- 실패 taxonomy, 역할 프롬프트, 문서, manifest, metadata, export를 `1.14.0`으로 동기화했다.

## 검증

| 검사 | 결과 |
|---|---:|
| Intent route matrix | 9/9 PASS |
| Context compounding acceptance | 33/33 PASS |
| Contract/BOM | 3/3 PASS |
| Workflow state | 2/2 PASS |
| Manuscript guard evidence | 2/2 PASS |
| 기존 project regression | 6/6 PASS |
| Agent registry audit | PASS |
| Package audit | PASS, warning 0 |
| Lexicon audit | PASS |
| Current-system alignment | PASS |
| Export build | PASS |
| Generated test report | PASS |

## 남은 차단 사항

다음은 시스템 코드 결함이 아니라 입력·콘텐츠 차단이다.

1. 4개 legacy sample original TXT가 없어 original-reference 평가는 계속 `CONTEXT_REQUIRED_MISSING`이다.
2. 공식 플랫폼 실시간 재조회는 실행 환경의 HTTP 403이 해제되어야 한다.
3. `sample_combined_episodes_01_10`은 `candidate_manuscript_chunk`이며 10화 전부 3,600자 미달이다. 원본 TXT가 없고 실제 `ai_tell_guard.py`도 없어 최종 원고로 승격하지 않았다. 시스템은 이 상태를 PASS로 숨기지 않고 계속 차단한다.


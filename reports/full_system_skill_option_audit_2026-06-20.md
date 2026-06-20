# WebNovel Production Loop 전수 감사

- 감사일: 2026-06-20
- 대상 버전: `1.13.0`
- 범위: 9개 intent, 13개 역할, 10개 control loop, 23개 Python 스크립트, 18개 schema, 30개 template, 83개 package asset, 3개 전문화 엔진과 4개 legacy sample loop
- 판정: **REQUEST CHANGES**
- 변경 정책: 이번 감사에서는 제품 코드와 정책을 수정하지 않았다.

## 실행 요약

| 영역 | 실제 실행 결과 |
|---|---|
| 프로젝트 계약 | valid PASS, invalid FAIL, IP pending 시 `IP_REVIEW_NOT_CLEARED` 검출 |
| 내러티브 | valid PASS, invalid PASS/FAIL 기대값 일치 |
| 회귀 | 6/6 PASS |
| Context Compounding | 12종 계약 검증 PASS, acceptance 22/22 PASS |
| Inner/State/Review/Control CLI | 정상 template PASS |
| Review Diff | 명시적 draft/final 생성 PASS, 반복 집계 실행 |
| State Commit | dry-run/실제 commit PASS |
| Replay | PASS, regression gate 동작 |
| Version Control | candidate/canary/promote 차단 조건 확인, rollback dry-run PASS |
| Workflow State | init/update/show/complete/blocked 실행 |
| Manuscript | guard 정상/차단 경로 확인, 3600자 길이 감사 실행 |
| Lexicon/Style/Semantic | audit PASS, style PASS, semantic average 4.08 PASS |
| Package | registry/package/alignment/export/report PASS |
| Legacy migration | 67 artifact overlay 생성 및 schema PASS |
| 전문화 샘플 | 4개 모두 원본 부재로 `CONTEXT_REQUIRED_MISSING` |
| 플랫폼 최신 조사 | 공식 웹 접근이 실행 환경의 HTTP 403으로 차단됨 |

## 발견 사항

### Critical

1. **승인된 canon delta가 적용되지 않아도 성공으로 보고된다.**
   - `episode_memory_delta` schema는 `canon_decision`을 허용한다.
   - `commit_episode_state.py:40-43`은 해당 타입을 `continue`로 버린다.
   - 실제 실행에서 canon 변경 1건은 schema PASS, commit PASS, `change_count: 1`, state version `0.1.1`로 상승했지만 canon 저장소에는 아무 변화도 없었다.
   - 영향: 승인된 정본 변경이 유실되고 성공 로그만 남는다.

### High

2. **Hook Judgment의 intent 경로가 현재 Step 번호와 불일치한다.**
   - `.codex/skills/webnovel-production-workflow/SKILL.md:20-24`는 drafting 4-7, rewrite 7, platform 1/8, ops 9, incident 10으로 안내한다.
   - 실제 단계는 Polish 6, Launch 7, Observe 8, Repair 9이며 Step 10은 없다.
   - 영향: rewrite가 Launch로, ops가 Repair로, incident가 존재하지 않는 단계로 라우팅될 수 있다.

3. **라우팅 계약이 문서에만 있고 결정적 router가 없다.**
   - 9개 intent를 schema가 받지만 intent→phase→role을 검증하는 실행 코드와 전수 route fixture가 없다.
   - 역할 prompt 13개는 독립 runtime agent가 아니라 Orchestrator가 해석해 호출하는 Markdown 계약이다.
   - 영향: 실제 호출 누락이나 잘못된 phase 진입을 package audit가 검출하지 못한다.

4. **Review Packet은 존재하지 않는 draft/final 파일로도 PASS한다.**
   - `audit_context_compounding.py:122`는 문자열 비어 있음/동일 여부만 검사한다.
   - 실제 `templates/review_packet.json`의 두 경로가 모두 없는데 review audit가 PASS했다.
   - 영향: 사람이 실제로 검토하지 않은 쌍으로 Outer Loop 근거를 만들 수 있다.

5. **Replay는 원고 파일과 hash를 확인하지 않고 호출자가 넣은 점수를 신뢰한다.**
   - `evaluate_change_replay.py:24-36`은 path를 열지 않는다.
   - 실제 current/candidate/human_final 파일 3개가 모두 없는데 replay가 PASS했다.
   - 영향: 허위 또는 stale 평가가 candidate 승격 근거가 될 수 있다.

6. **동일 Review ID 복제로 반복 기준 3회를 충족할 수 있다.**
   - `analyze_review_diff.py:63-85`는 schema 검증과 `review_id` 중복 제거가 없다.
   - 동일 JSON을 세 파일로 복제하자 `completed_reviews_considered: 3`, `promotable_candidate_count: 1`로 PASS했다.
   - 영향: 단 한 번의 수정이 시스템 개선 후보로 승격된다.

7. **캐릭터·관계·역할극 ID 중복 및 지식 누출을 검출하지 못한다.**
   - state schema 배열에는 ID 단위 uniqueness가 없다.
   - duplicate character, duplicate relationship, duplicate participant를 넣고 다른 인물에게 비밀을 known fact로 추가해도 state audit가 PASS했다.
   - 영향: 3인 이상 장면의 지식·관계 일관성 완료 조건을 충족하지 못한다.

8. **중복 Evidence `context_id`가 충돌을 숨긴다.**
   - `audit_context_compounding.py:64`가 dict comprehension으로 마지막 값을 덮어쓴다.
   - 같은 context ID의 상충된 resolved evidence를 추가해도 Inner audit가 PASS했다.
   - 영향: 정본 근거 충돌이 Writer 차단을 우회할 수 있다.

9. **사람 문체 보정 완료가 검증되지 않고 CLI flag만 신뢰된다.**
   - `run_manuscript_guard.py:23,55`의 `--humanized`는 artifact/hash 없이 호출자 선언만 확인한다.
   - 영향: `$humanize-korean` 미실행 원고도 완료 gate를 통과할 수 있다.

10. **현재 프로젝트 회차 10개가 모두 필수 3600자 미달이다.**
    - `projects/sample_combined_episodes_01_10/episode_001.txt`~`010.txt` 전부 FAIL.
    - 공백 제외 최저 632자, 최고 773자이며 각 화 2,827~2,968자 부족하다.
    - 영향: 패키지는 PASS지만 현재 산출물은 명시된 원고 완료 조건을 충족하지 않는다.

11. **workflow state가 유한상태기계 불변식을 강제하지 않는다.**
    - `workflow_state.py:113-118`은 complete와 blocked를 단순 필드 변경으로 처리한다.
    - 실제 완료(`active:false`, `PASS`) 후 blocked 전이가 허용되어 `active:false`, `PASS`, blocked reason이 동시에 남았다.
    - 또한 Context Plan/Evidence/Review/Proposal/Canary/Approval 상태를 저장하지 않는다.
    - 영향: resume 시 제어 루프의 실제 단계와 승인 상태를 재구성할 수 없다.

12. **신규 Context Compounding가 project/output 최상위 완료 계약에 강제되지 않는다.**
    - `project.schema.json:34`의 `context_compounding`은 선택 항목이다.
    - `output.schema.json:6`은 status/phase/artifacts/validation만 필수다.
    - valid fixture는 current evidence/state/review/version 정보 없이 PASS한다.
    - 영향: 새 시스템을 완전히 건너뛴 실행도 공식 PASS 출력이 가능하다.

13. **회귀 범위가 실제 선택 공간보다 작다.**
    - 회귀 fixture는 6개뿐이며 9 intent, 13 role, route table, rights route, 파일 실재성, ID 중복, canon delta를 전수하지 않는다.
    - `TEST_REPORT.json` PASS는 이 제한된 subset의 성공이다.
    - 영향: package/registry/alignment audit가 모두 PASS해도 위 결함들이 남는다.

### Medium

14. **state commit이 변경 근거를 갱신하지 않는다.**
    - `commit_episode_state.py:48-53`은 값과 version/episode만 바꾸며 `last_evidence`를 delta source로 갱신하지 않는다.
    - 영향: 변경 후 provenance가 이전 Story Bible 근거를 계속 가리킨다.

15. **state commit과 version manager가 입력 schema를 자체 검증하지 않는다.**
    - 두 스크립트는 JSON parse 후 필드 접근/상태 전이만 수행한다.
    - 영향: 별도 validate 단계가 누락되면 malformed artifact가 부분 처리될 수 있다.

16. **Rollback은 회귀 증거나 승인 없이도 실행된다.**
    - `manage_component_versions.py:64-68`은 previous version 존재만 확인한다.
    - pending proposal로 rollback dry-run이 PASS했다.
    - 영향: “회귀 발생 시 즉시 복귀” 외의 임의 상태 변경을 정책적으로 구분하지 못한다.

17. **Windows UTF-8 BOM 입력 호환성이 일관되지 않다.**
    - PowerShell `Set-Content -Encoding UTF8`로 만든 유효 JSON을 `validate_project.py`가 BOM 오류로 거부했다.
    - 일부 다른 스크립트는 `utf-8-sig`를 사용한다.
    - 영향: Windows 기본 작업 흐름에서 유효 파일이 INPUT 실패할 수 있다.

18. **PowerShell 콘솔에서 한국어가 mojibake로 표시되는 경로가 남아 있다.**
    - Python validator 자체는 UTF-8로 정상 처리하지만 `Get-Content`/캡처 조합에서 fixture와 lexicon 한국어가 손상 표시된다.
    - 영향: 사람이 콘솔 결과를 근거로 잘못 판단할 위험이 있다.

19. **legacy source availability가 `policy` kind로 오분류된다.**
    - `context_plan.schema.json:21`에 `source_availability`가 없다.
    - `migrate_legacy_context_data.py:56`은 원본 존재 여부를 `policy`로 기록한다.
    - 영향: 검색/정책/자료 가용성 실패 통계가 섞인다.

20. **Story Bible이 없는 legacy sample에도 임시 문자열 버전을 강제한다.**
    - evidence schema는 non-empty `story_bible_version`을 요구한다.
    - 4개 overlay는 `not_available_legacy_sample`을 사용한다.
    - 영향: 실제 정본 version과 “해당 없음” sentinel을 같은 필드에서 구분하기 어렵다.

21. **Review Diff 분류는 분석 결과가 아니라 호출자 입력이다.**
    - `analyze_review_diff.py:37-55`는 허용 enum과 가설 개수만 확인한다.
    - 영향: Review Diff Analyst의 의미 분류 정확성을 결정적으로 검증하지 못한다.

### Blocked / External

22. **4개 전문화 sample loop의 original-reference 평가가 차단됐다.**
    - `muhan_regression`, `dimension_transfer`, `transcendent_gallery`, `vampire_constraint` 모두 `CONTEXT_REQUIRED_MISSING`.
    - 파생 reference와 recreation은 존재하지만 원본 TXT가 없어 구조·효과 비교를 완료할 수 없다.

23. **공식 플랫폼 정보 refresh가 이 실행 환경의 HTTP 403으로 차단됐다.**
    - 로컬 profile freshness는 4일/TTL 30일로 PASS했다.
    - 하지만 공식 사이트를 직접 재검증하지 못했으므로 최신 사실 확인은 완료로 간주할 수 없다.

## 정상 동작이 확인된 방어선

- 필수 context 누락, stale context, unresolved conflict는 Writer 전 gate에서 차단된다.
- 승인되지 않은 delta와 base version drift는 commit을 차단한다.
- draft/final 동일 경로와 가설 3개 미만은 Review Diff 생성을 차단한다.
- 승인 없는 candidate, candidate 없는 canary, passing canary 없는 promote는 차단된다.
- IP review pending은 launch validation을 차단한다.
- package audit, role registry audit, lexicon audit, style audit, semantic rubric, export build는 현재 fixture 기준 PASS한다.

## 우선순위

1. canon delta silent drop 제거 및 정본 변경 저장소를 명시한다.
2. Review/Replay 파일 실재성·hash·고유 review ID를 promotion 전 강제한다.
3. Hook Judgment step 번호와 결정적 router/route tests를 동기화한다.
4. character/relationship/participant/evidence ID uniqueness와 knowledge-boundary 검사를 추가한다.
5. Context Compounding 상태를 project/output/workflow state의 필수 계약으로 승격한다.
6. 9 intent × 13 role × 주요 gate의 route/negative regression matrix를 추가한다.
7. 현재 10개 회차를 3600자 gate에 맞게 별도 보강한다.


# 비교대출 완료 추첨 포인트 지급 이벤트 (7월) — 테스트 케이스

| Date | Action | TC_ID | Writer |
|------|--------|-------|--------|
| 2026-06-26 | 신규 작성 | 전체 | Claude (FQA-2259) |

---

## 커버리지 요약

| 카테고리 | TC 수 |
|---------|------|
| 프로모션 인트로 | 7 |
| 추첨 결과 — FINDA_POINT | 4 |
| 추첨 결과 — VOUCHER | 3 |
| **합계** | **14** |

| 우선순위 | 수 |
|---------|---|
| High | 7 |
| Medium | 5 |
| Low | 2 |

> ※ U1(참여 완료 유저 재방문), U3(FINDA_POINT 화면 구성) 확정 시 TC 추가 예정.
> ※ 본인인증 화면 TC 미생성 (U6: 기존 한도조회 공용 화면).

---

## 프로모션 인트로

| TC_ID | Category1 | Category2 | Category3 | Level | pre-Condition | Test Procedure | Expected Result | Android | iOS | Comment |
|-------|-----------|-----------|-----------|-------|--------------|----------------|----------------|---------|-----|---------|
| TC-01-01 | 프로모션 인트로 | — | — | High | CRM PUSH 수신 (이벤트 기간 내) | 1. CRM 메시지 선택 | 프로모션 인트로 이동 | | | |
| TC-01-02 | 프로모션 인트로 | — | — | High | 스마트배너 노출 (이벤트 기간 내) | 1. 스마트배너 선택 | 프로모션 인트로 이동 | | | |
| TC-01-03 | 프로모션 인트로 | — | — | High | 핀다소식탭 진입 (이벤트 기간 내) | 1. 이벤트 영역 선택 | 프로모션 인트로 이동 | | | |
| TC-01-04 | 프로모션 인트로 | — | — | Medium | 프로모션 인트로 진입 | 1. 화면 구성 확인 | 뒤로가기 버튼 노출<br>[안내] 버튼 노출 | | | OK7 |
| TC-01-05 | 프로모션 인트로 | — | — | Medium | 프로모션 인트로 진입 | 1. 뒤로가기 버튼 선택 | 이전 화면으로 이동 | | | OK7 |
| TC-01-06 | 프로모션 인트로 | 안내 바텀싯 | — | Medium | 프로모션 인트로 진입 | 1. [안내] 버튼 선택 | 안내 바텀싯 노출 | | | OK4 |
| TC-01-07 | 프로모션 인트로 | 안내 바텀싯 | — | Low | 안내 바텀싯 노출 상태 | 1. 닫기 선택 | 바텀싯 닫힘<br>프로모션 인트로 유지 | | | OK4 |

> ※ [미정의 — U1] 이미 참여 완료한 유저가 프로모션 인트로 재방문 시 화면 상태 — 정책 확인 후 TC 추가 예정.

---

## 추첨 결과 — FINDA_POINT (랜덤 포인트 즉시 지급)

> ※ [미정의 — U3] 화면 구성 상세는 Figma 확인 후 기대 결과 보강 예정.

| TC_ID | Category1 | Category2 | Category3 | Level | pre-Condition | Test Procedure | Expected Result | Android | iOS | Comment |
|-------|-----------|-----------|-----------|-------|--------------|----------------|----------------|---------|-----|---------|
| TC-02-01 | 추첨 결과 | FINDA_POINT | — | High | 미참여 유저, 본인인증 완료 (`rewardItemType=FINDA_POINT`) | 1. 추첨 결과 화면 진입 | FINDA_POINT 당첨 결과 화면 노출<br>즉시 지급 포인트(100~1,000P) 표시 | | | C1 결정: rewardItemType 기준 |
| TC-02-02 | 추첨 결과 | FINDA_POINT | — | High | FINDA_POINT 결과 화면 진입 (`rewardItemType=FINDA_POINT`), 가승인 유저 | 1. CTA 선택 | 가승인 화면으로 이동 | | | OK2 |
| TC-02-03 | 추첨 결과 | FINDA_POINT | — | High | FINDA_POINT 결과 화면 진입 (`rewardItemType=FINDA_POINT`), 올거절 유저 | 1. CTA 선택 | 올거절 화면으로 이동 | | | OK2 |
| TC-02-04 | 추첨 결과 | FINDA_POINT | — | Low | 전체 기간 내 동일 CI로 재참여 시도 | 1. 참여 흐름 재진입 | 중복 참여 차단 안내 노출 | | | OK3: CI 기준 전체 기간 1회 |

---

## 추첨 결과 — VOUCHER (10만P 수기 지급)

| TC_ID | Category1 | Category2 | Category3 | Level | pre-Condition | Test Procedure | Expected Result | Android | iOS | Comment |
|-------|-----------|-----------|-----------|-------|--------------|----------------|----------------|---------|-----|---------|
| TC-03-01 | 추첨 결과 | VOUCHER | — | High | 미참여 유저, 본인인증 완료 (`rewardItemType=VOUCHER`) | 1. 추첨 결과 화면 진입 | VOUCHER 당첨 결과 화면 노출<br>10만P 즉시 지급이 아님을 안내하는 문구 노출 | | | C1 결정: rewardItemType 기준; OK6 |
| TC-03-02 | 추첨 결과 | VOUCHER | — | Medium | VOUCHER 결과 화면 진입 (`rewardItemType=VOUCHER`), 가승인 유저 | 1. CTA 선택 | 가승인 화면으로 이동 | | | OK2 |
| TC-03-03 | 추첨 결과 | VOUCHER | — | Medium | VOUCHER 결과 화면 진입 (`rewardItemType=VOUCHER`), 올거절 유저 | 1. CTA 선택 | 올거절 화면으로 이동 | | | OK2 |

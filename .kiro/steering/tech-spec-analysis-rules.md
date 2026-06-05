# Tech Spec 분석 규칙

## 개요

Tech Spec은 개발 조직이 작성한 API 기반 기술 문서다. QA 관점에서 TC의 사전 조건 정밀화, 분기 조건 명확화, 에러 케이스 발견에 활용한다.

## 개발 조직 구분

| 조직 | 역할 | Tech Spec 내용 |
|------|------|---------------|
| Jupiter | Backend | 서버 API 엔드포인트, 비즈니스 로직, 데이터 처리 |
| Earth | Backend | 서버 API 엔드포인트, 외부 연동, 데이터 저장 |
| Web | Frontend | 화면 연동 로직, 프론트 분기 처리, UI 상태 변경 규칙 |

## 분석 대상

Tech Spec에서 다음 항목을 추출한다:

### Backend Tech Spec (Jupiter/Earth)에서 추출

1. **API 엔드포인트 목록** — URL, HTTP Method, 호출 시점
2. **요청/응답 파라미터** — 필드명, 타입, 의미
3. **분기 조건** — 응답값 기반 화면 분기 (예: `rewardItemType = VOUCHER → 당첨 페이지`)
4. **에러 응답** — 에러 코드, 에러 메시지, 처리 방식
5. **상태 판정 로직** — 참여 여부, 자격 조건, 중복 방지 등
6. **외부 연동** — 3rd party API (나이스디앤알 등), 연동 실패 시 처리
7. **Enum 정의** — 분기에 사용되는 상수값 목록

### Frontend Tech Spec (Web)에서 추출

1. **화면-API 매핑** — 어떤 화면에서 어떤 API를 호출하는지
2. **프론트 유효성 검증** — 입력값 검증 규칙, CTA 활성/비활성 조건
3. **UI 상태 전이** — API 응답에 따른 화면 변경
4. **로딩/에러 처리** — API 호출 중 UI 상태, 실패 시 화면 처리
5. **이중 클릭 방지** — CTA disabled 처리 조건

## TC 반영 규칙

### pre-Condition에 반영

Tech Spec의 API 상태 조건을 TC의 사전 조건에 구체적으로 반영한다.

| Tech Spec 정보 | pre-Condition 반영 방식 |
|---------------|------------------------|
| `isJoined = true` | "이미 프로모션에 참여 완료한 유저 (`isJoined=true`)" |
| `rewardItemType = VOUCHER` | "추첨 결과가 주유권 당첨인 경우 (`rewardItemType=VOUCHER`)" |
| 특정 에러 코드 반환 상태 | "본인 명의 확인 실패 상태 (API 에러 응답)" |

**작성 규칙:**
- 괄호 안에 API 필드/값을 병기하여 테스트 환경 세팅 시 참고할 수 있게 한다.
- 사전 조건의 주 표현은 여전히 비즈니스 언어로 작성하고, API 값은 보조 정보로 괄호 처리한다.

### Expected Result에는 직접 반영하지 않음

- 기대 결과는 여전히 **사용자가 화면에서 인지할 수 있는 것**으로 작성한다.
- API 응답값 자체를 기대 결과에 넣지 않는다.
- 단, API 응답값에 의한 **화면 분기 결과**는 기대 결과에 반영한다.

### ❌ Bad
```
• API 응답의 rewardItemType이 VOUCHER임
• isCompleted = true 반환됨
```

### ✅ Good
```
• 주유권 당첨 페이지로 이동
• "참여가 완료되었습니다" 안내 메시지 노출
```

### Comment에 반영

- TC의 Comment 열에 연관 API 정보를 간략히 기재할 수 있다.
- 형식: `API: {METHOD} {endpoint}` (예: `API: POST /pcs/challenge/v1/action/perform`)
- QA 실행 시 네트워크 탭에서 해당 API 호출을 확인하는 참고 정보로 활용.

## 통합 명세 반영

Tech Spec 분석 결과는 통합 명세의 **"7. 기술 요구사항"** 섹션에 다음 구조로 반영한다:

```markdown
## 7. 기술 요구사항

### API 엔드포인트

| 화면/액션 | API | Method | 주요 파라미터 | 분기 조건 |
|-----------|-----|--------|-------------|----------|
| 프로모션 진입 | /pcs/challenge/v1/{key}/is-joined | GET | - | isJoined로 참여 여부 판정 |
| 약관 동의 CTA | /pcs/challenge/v1/{key}/join | POST | - | 성공 시 추첨 단계로 이동 |
| 주유권 추첨 | /pcs/challenge/v1/action/perform | POST | eventName | rewardItemType으로 결과 분기 |

### 응답값 기반 화면 분기

| 응답 필드 | 값 | 화면 분기 |
|-----------|---|----------|
| rewardItemType | VOUCHER | 주유권 당첨 페이지 |
| rewardItemType | FINDA_POINT | 포인트 지급 페이지 |

### 에러 처리

| 에러 상황 | 처리 방식 | 화면 |
|-----------|----------|------|
| API 호출 실패 | 에러 팝업 노출 | 오류 안내 팝업 |

### 외부 연동

| 연동 대상 | 용도 | 실패 시 처리 |
|-----------|------|-------------|
| 나이스디앤알 | 본인 명의 확인 | 에러 팝업 |
```

## 이해충돌 검토 시 활용

Tech Spec 정보는 이해충돌 검토에서 다음과 같이 활용한다:

| 검토 항목 | 예시 |
|-----------|------|
| PRD의 분기 조건 vs Tech Spec의 API 분기값 | PRD: "당첨/미당첨" → Tech Spec: `VOUCHER/FINDA_POINT` (미당첨이 아니라 포인트 지급) |
| PRD의 에러 정책 vs Tech Spec의 에러 코드 | PRD: "에러 시 팝업" → Tech Spec에 에러 코드 5종 정의 (동일 처리인지 확인) |
| 피그마 화면 수 vs Tech Spec 분기값 수 | 피그마에 결과 화면 2개 → Tech Spec enum 3종 (누락 화면 없는지) |

- Tech Spec에만 존재하고 PRD/피그마에 없는 분기 → 미정의 항목으로 등록
- PRD/피그마의 분기가 Tech Spec과 불일치 → 충돌 항목으로 등록

## 주의사항

- Tech Spec의 **내부 구현 디테일**은 TC에 반영하지 않는다:
  - DB 스키마, 테이블명, 컬럼명
  - 내부 함수명, 클래스명
  - 서버 내부 로직 순서 (유저에게 보이지 않는 처리)
  - 인프라 구성 (서버 배포, 캐시 전략 등)
- Tech Spec은 **사전 조건 정밀화**와 **에러/분기 케이스 발견**에 한정하여 활용한다.
- Tech Spec에만 정의되고 PRD/피그마에 반영되지 않은 동작은 TC에 넣지 않고, 이해충돌 체크리스트의 미정의 항목으로 등록한다.

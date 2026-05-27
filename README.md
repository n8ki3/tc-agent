# QA TC Generator Agent

PRD(기획문서)와 Figma 디자인을 분석하여 테스트 케이스를 자동 생성하는 Kiro 에이전트입니다.

## 기능

- **PRD 분석**: 화면 정책, 비즈니스 규칙, 에러 정책, API, 이벤트 로그 자동 추출
- **Figma 분석**: 화면 프레임, 플로우차트, annotations, 핸드오프 노트 확인
- **이해충돌 검토**: PRD-피그마 간 충돌/미정의 항목을 체크리스트로 제시
- **TC 생성**: 근거 기반 테스트 케이스 (md + html 동시 생성)

---

## 설치

```bash
git clone https://github.com/n8ki3/tc-agent.git
```

clone한 폴더를 **Kiro IDE에서 워크스페이스로 열기**만 하면 준비 완료입니다.

## 사전 요구사항

- [Kiro IDE](https://kiro.dev) 설치
- Figma 계정 (최초 1회 OAuth 인증 필요)

---

## 사용 방법

### 1. Kiro에서 이 폴더를 워크스페이스로 열기

### 2. Figma MCP 연결 (최초 1회)

Kiro 좌측 패널에서 MCP Server 뷰를 열고, `figma` 서버의 연결 버튼을 클릭하여 OAuth 인증을 완료합니다.

### 3. 채팅에서 요청하기

Kiro 채팅창에 PRD 파일을 첨부하고, Figma 링크와 함께 요청하면 됩니다.

#### 예시 1: PRD + Figma 둘 다 제공

```
[PDF 파일 첨부]

이 PRD 기반으로 TC 생성해줘.
피그마 링크: https://www.figma.com/design/ABC123/파일명?node-id=726-8226&m=dev
```

#### 예시 2: PRD만 제공

```
[PDF 파일 첨부]

이 기획문서 분석해서 테스트 케이스 만들어줘.
```

#### 예시 3: Figma만 제공

```
이 피그마 디자인 분석해서 TC 뽑아줘.
https://www.figma.com/design/ABC123/파일명?node-id=726-8226&m=dev
```

#### 예시 4: 기존 명세 업데이트

```
[PDF 파일 첨부]

PRD가 업데이트됐어. 기존 명세랑 비교해서 변경된 부분 반영해줘.
```

### 4. 이해충돌 체크리스트 확정

에이전트가 분석을 마치면 충돌/미정의 항목을 체크리스트로 보여줍니다.
각 항목에 대해 선택해주세요:

```
## 이해충돌 검토 결과

### 충돌 항목
- [ ] #1: PRD에서 할인율형 폐기인데 피그마에 잔존 → PRD 기준 / 피그마 기준 / 확인 필요

### 미정의 항목
- [ ] #2: 스낵바 자동 사라짐 시간 → 정책 확인 필요 / TC에서 제외
```

→ "1번은 PRD 기준, 2번은 TC에서 제외" 이런 식으로 답변하면 됩니다.

### 5. 결과물 확인

확정 후 자동으로 생성됩니다:

| 파일 | 설명 |
|------|------|
| `aidlc-docs/features/{피처명}.md` | 통합 명세 |
| `aidlc-docs/features/{피처명}-test-cases.md` | TC (마크다운) |
| `aidlc-docs/features/{피처명}-test-cases.html` | TC (브라우저에서 열어보기) |

---

## 워크플로우 상세

```
입력 수집 (PRD + Figma)
  │
  ▼
PRD 분석 (정책, 규칙, API, 이벤트 추출)
  │
  ▼
Figma 분석 (화면, 플로우차트, annotations)
  │
  ▼
이해충돌 검토 → 체크리스트 제시 → 사용자 확정
  │
  ▼
통합 명세 생성
  │
  ▼
TC 생성 (md + html 동시)
```

---

## TC 작성 핵심 규칙

이 에이전트가 따르는 규칙입니다:

- ✅ 기대 결과는 사용자가 화면에서 인지할 수 있는 요소만 작성
- ✅ PRD/피그마에 명시된 근거가 있는 내용만 포함
- ❌ 디자인 디테일(px, 색상, 좌표 등) 제외
- ❌ 근거 없는 추측 금지
- ❌ 에러 정책이 하나로 커버되면 원인별 TC 분리하지 않음
- 📌 미정의 항목은 `[미정의]` 태그로 분리하여 별도 관리

---

## 프로젝트 구조

```
qa-tc-agent/
├── .kiro/
│   ├── agents/
│   │   └── qa-tc-generator.md      ← 에이전트 정의
│   ├── settings/
│   │   └── mcp.json                ← Figma MCP 설정
│   └── steering/
│       ├── qa-workflow.md           ← 전체 워크플로우
│       ├── prd-analysis-rules.md    ← PRD 분석 규칙
│       ├── figma-analysis-rules.md  ← Figma 분석 규칙
│       ├── test-case-rules.md       ← TC 작성 규칙
│       └── language.md              ← 한국어 응답
├── aidlc-docs/features/             ← 생성된 결과물 저장 위치
├── examples/coupon-box/             ← 예시 결과물
└── README.md
```

---

## 예시 결과물

`examples/coupon-box/` 폴더에 실제 피처(쿠폰함 개선)를 분석한 결과물이 포함되어 있습니다. 어떤 형태로 결과가 나오는지 참고하세요.

---

## 규칙 커스터마이징

`.kiro/steering/` 폴더의 md 파일들을 수정하면 에이전트 동작을 조정할 수 있습니다:

- TC 작성 규칙 변경 → `test-case-rules.md` 수정
- 분석 범위 조정 → `prd-analysis-rules.md` 또는 `figma-analysis-rules.md` 수정
- 워크플로우 단계 변경 → `qa-workflow.md` 수정

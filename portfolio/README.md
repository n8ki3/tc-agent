# QA TC Generator Agent — 포트폴리오

## 프로젝트 개요

PRD(기획문서)와 Figma 디자인을 입력받아 **근거 기반 테스트 케이스를 자동 생성**하는 AI 에이전트입니다.

QA 엔지니어의 분석 프로세스를 체계화하여, 기획-디자인 간 불일치를 사전에 발견하고 추측 없는 테스트 케이스를 생성합니다.

---

## 만든 이유

| 문제 | 해결 |
|------|------|
| PRD와 Figma 간 정책 불일치를 QA 단계에서야 발견 | 분석 단계에서 자동으로 충돌 검출 → 인터랙티브 체크리스트로 제시 |
| TC 작성 시 근거 없는 추측이 섞임 | "근거 기반 원칙" 규칙으로 명세에 없는 내용 자동 차단 |
| TC 형식이 작성자마다 달라 리뷰 비용 증가 | 일관된 구조 + md/html 동시 생성으로 표준화 |
| 디자인 디테일(px, 색상)이 TC에 섞여 유지보수 어려움 | "사용자 인지 가능 요소"만 기대 결과에 포함하는 규칙 |
| 분석 결과가 대화창에 흩어져 추적 불가 | 피처별 폴더에 4종 산출물 세트로 파일 관리 |

---

## 핵심 설계 원칙

### 1. 근거 기반 (Evidence-Based)

TC의 모든 기대 결과는 PRD, 피그마, 확정된 정책 문서에서 확인 가능해야 합니다. 업계 관행이나 유사 서비스 유추로 채우지 않습니다.

```
✅ 근거 인정: PRD 텍스트, 피그마 UI 요소, 플로우차트 화살표, 핸드오프 노트
❌ 근거 불인정: 업계 관행, 유사 서비스 유추, 기술적 구현 가정
```

### 2. 사용자 확정 게이트 (Human-in-the-Loop)

PRD-피그마 간 충돌이나 미정의 항목을 발견하면, **인터랙티브 HTML 체크리스트**를 생성하여 사용자가 브라우저에서 직접 확정합니다. 확정 전까지 다음 단계로 진행하지 않습니다.

### 3. 미정의 항목 분리

명세에 없지만 검증이 필요한 동작은 `[미정의]` 태그로 분리하여 PO/개발에 확인을 요청합니다. 추측으로 채우지 않고, 모르는 것은 모른다고 표시합니다.

### 4. 피처별 산출물 세트

모든 분석 결과는 대화창이 아닌 **파일**로 관리합니다. 피처당 4개 파일이 한 세트:

```
aidlc-docs/features/{feature-name}/
├── {feature-name}.md                  ← 통합 명세
├── {feature-name}-checklist.html      ← 이해충돌 체크리스트 (인터랙티브)
├── {feature-name}-test-cases.md       ← TC 마크다운
└── {feature-name}-test-cases.html     ← TC HTML (브라우저 뷰)
```

---

## 워크플로우

```
┌─────────────────────────────────────────────────────┐
│  입력: PRD (PDF/Confluence) + Figma 링크             │
└──────────────────────┬──────────────────────────────┘
                       │
          ┌────────────┴────────────┐
          ▼                         ▼
┌─────────────────┐      ┌─────────────────────┐
│  Step 1.        │      │  Step 2.            │
│  PRD 분석       │      │  Figma 분석         │
│  (Confluence    │      │  (Figma MCP)        │
│   API 활용)     │      │                     │
└────────┬────────┘      └──────────┬──────────┘
         │                          │
         └────────────┬─────────────┘
                      ▼
┌──────────────────────────────────────────────────────┐
│  Step 3. 이해충돌 검토                                │
│  → {feature-name}-checklist.html 생성                │
│  → 브라우저에서 사용자 확정                            │
└──────────────────────┬───────────────────────────────┘
                       │ (사용자 확정 결과 입력)
                       ▼
┌──────────────────────────────────────────────────────┐
│  Step 4. 통합 명세 생성                               │
│  → {feature-name}.md                                 │
└──────────────────────┬───────────────────────────────┘
                       │
                       ▼
┌──────────────────────────────────────────────────────┐
│  Step 5. TC 생성 (md + html 동시)                     │
│  → {feature-name}-test-cases.md                      │
│  → {feature-name}-test-cases.html                    │
└──────────────────────────────────────────────────────┘
```

---

## 실제 실행 사례

### 사례 1: 쿠폰함 개선 (coupon-box)

| 항목 | 내용 |
|------|------|
| 입력 | PRD v1.4 (PDF) + Figma 7개 화면 |
| 산출물 | 통합 명세 + TC 26건 (Critical 6 / High 12 / Medium 8) |
| 위치 | `aidlc-docs/features/coupon-box/` |

### 사례 2: 차번호 입력 프로모션 (car-number-promo)

| 항목 | 내용 |
|------|------|
| 입력 | Confluence PRD v3.1 (API 연동) + Figma 9개 화면 + User Flow |
| 산출물 | 통합 명세 + 체크리스트 HTML + TC 36건 (Critical 12 / High 21 / Medium 3) |
| 위치 | `aidlc-docs/features/car-number-promo/` |
| 특이사항 | PRD 업데이트 반영 (이해충돌 확정 후 추가 정책 변경 즉시 반영) |

#### 차번호 프로모션 — 실행 과정 요약

1. **Confluence API로 PRD 자동 수집** — 사용자가 URL + 인증 정보 제공 → API 호출로 HTML 파싱
2. **Figma MCP로 디자인 분석** — `get_metadata` → `get_screenshot` → `get_design_context`로 9개 화면 + User Flow + 유의사항 텍스트 추출
3. **이해충돌 10건 발견** — 팝업 X 버튼 유무, CTA 문구 불일치, 동의서 종속 관계 등
4. **인터랙티브 체크리스트 생성** — 브라우저에서 사용자가 10건 모두 확정
5. **TC 36건 생성** — 확정 결과 기반, 근거 없는 추측 0건
6. **PRD 업데이트 즉시 반영** — 이후 추가 정책 변경(상단 네비게이션 변경, 유효성 검증 방식 변경 등) 수신 → 명세 + TC 동시 업데이트

---

## 기술 스택 & 아키텍처

| 구성 요소 | 역할 |
|----------|------|
| **Kiro IDE** | AI 에이전트 실행 환경 (Agent + Steering 시스템) |
| **Figma MCP** | Figma 디자인 파일 읽기 (get_metadata, get_design_context, get_screenshot) |
| **Confluence API** | PRD 문서 자동 수집 (REST API + 인증) |
| **Steering Files** | 에이전트 행동 규칙 정의 (5개 규칙 파일) |

### 프로젝트 구조

```
qa-tc-agent/
├── .kiro/
│   ├── settings/mcp.json              ← Figma MCP 연결 설정
│   └── steering/                      ← 행동 규칙 (5개)
│       ├── qa-workflow.md             ← 전체 작업 흐름 + 산출물 규칙
│       ├── prd-analysis-rules.md      ← PRD 분석 규칙
│       ├── figma-analysis-rules.md    ← Figma 분석 규칙
│       ├── test-case-rules.md         ← TC 작성 규칙 + 산출물 형식
│       └── language.md                ← 한국어 응답
├── aidlc-docs/features/               ← 피처별 산출물 폴더
│   ├── car-number-promo/              ← 4종 세트
│   └── coupon-box/                    ← 3종 (체크리스트 이전 작업)
├── examples/coupon-box/               ← 출력 형식 템플릿
└── portfolio/                         ← 이 문서
```

---

## 규칙 설계 상세

### Steering 파일 간 관계

```
qa-workflow.md (전체 흐름 오케스트레이션 + 산출물 규칙)
  ├── prd-analysis-rules.md (Step 1에서 참조)
  ├── figma-analysis-rules.md (Step 2에서 참조)
  └── test-case-rules.md (Step 5에서 참조 + 산출물 형식 정의)
```

### 주요 규칙 요약

| 규칙 파일 | 핵심 내용 |
|----------|----------|
| `qa-workflow.md` | 7단계 워크플로우, 산출물 규칙(파일로 떨구기), 이해충돌 검토 방식 |
| `prd-analysis-rules.md` | 취소선=폐기, TBD=미확정, 최신 버전 우선, 회의록은 확정 결론만 |
| `figma-analysis-rules.md` | Handoff 노트 필수 확인, 플로우차트 분기 추출, 기존 명세와 충돌 검토 |
| `test-case-rules.md` | 근거 기반 원칙, 디자인 디테일 제외, TC 분리 기준, 산출물 4종 형식, 피처별 폴더 구조 |

### 산출물 형식 규칙 (test-case-rules.md에 정의)

| 산출물 | 형식 규칙 |
|--------|----------|
| 통합 명세 | 8개 섹션 구조 (목표 → 스킴 → Flow → 화면정책 → 리워드 → 로그 → 기술 → 미결) |
| 체크리스트 HTML | 충돌/미정의/일치 섹션 분리, 옵션 버튼, 로컬스토리지 저장, 내보내기 기능 |
| TC md | 카테고리별 테이블, 커버리지 요약 포함 |
| TC html | examples 템플릿 CSS 준수, 뱃지 색상 통일 |

---

## 이 프로젝트에서 보여주고 싶은 것

### QA 역량

- 기획-디자인 간 불일치를 체계적으로 발견하는 분석 프로세스 설계
- "추측 금지" 원칙으로 TC 품질 기준 정립
- 미정의 항목을 명시적으로 분리하여 커뮤니케이션 비용 절감
- PRD 업데이트를 즉시 반영하는 살아있는 문서 관리

### 자동화 & 도구 설계 역량

- AI 에이전트의 행동을 규칙 파일로 제어하는 아키텍처 설계
- Figma MCP + Confluence API를 활용한 다중 소스 자동 분석 파이프라인
- Human-in-the-Loop 패턴으로 자동화와 판단의 균형 설계
- 인터랙티브 HTML 체크리스트로 비개발자도 사용 가능한 확정 UX

### 문서화 & 프로세스 역량

- 워크플로우를 단계별로 분리하고 각 단계의 입출력을 명확히 정의
- 규칙 간 참조 관계를 설계하여 유지보수 가능한 구조 구현
- 피처별 폴더 + 4종 세트로 산출물 추적성 확보

---

## 실행 방법

```bash
# 1. 클론
git clone https://github.com/n8ki3/tc-agent.git

# 2. Kiro IDE에서 워크스페이스로 열기

# 3. Figma MCP 연결 (좌측 패널 → MCP Server → figma 연결)

# 4. 채팅에서 요청
#    예: "새 피처 분석해줘. PRD: [Confluence URL], Figma: [Figma URL]"
```

---

## 링크

- **GitHub**: https://github.com/n8ki3/tc-agent
- **사용 도구**: [Kiro IDE](https://kiro.dev) + [Figma MCP](https://mcp.figma.com)
- **웹 애플리케이션 계획**: [webapp-portfolio.md](./webapp-portfolio.md)

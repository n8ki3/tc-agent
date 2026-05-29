# QA TC Generator Agent — 포트폴리오

> PRD와 피그마를 넣으면 근거 기반 테스트 케이스가 나옵니다. 추측은 안 합니다.

---

## 만든 것

PRD(기획문서)와 Figma 디자인을 동시에 분석해서 테스트 케이스를 자동 생성하는 AI 에이전트입니다.

기획-디자인 간 불일치를 사전에 잡아내고, 사용자가 확정한 뒤에야 TC를 만듭니다.
"일반적으로 이렇게 동작할 것이다"로 채운 TC는 하나도 없습니다.

---

## 왜 이렇게 만들었나

TC 작성할 때 반복되는 문제들:

1. PRD에는 A라고 써있는데 피그마에는 B로 그려져 있음 → QA 단계에서야 발견
2. "보통 이렇게 동작하겠지"로 채운 기대 결과 → 리뷰 때 "이거 어디 근거?" 질문
3. 작성자마다 형식이 달라서 리뷰 비용이 큼
4. 디자인 디테일(px, 색상코드)이 TC에 섞여서 UI 바뀔 때마다 TC도 수정

그래서 네 가지를 해결하는 구조를 잡았습니다:

- PRD + 피그마를 동시에 분석 → 충돌을 자동으로 찾아냄
- 충돌/미정의 항목은 인터랙티브 체크리스트로 사용자에게 확정 요청
- 확정된 내용만 TC에 반영 → 추측 제로
- 산출물 형식을 규칙으로 고정 → 누가 돌려도 같은 구조

---

## 동작 방식

```
PRD (PDF/Confluence) + Figma 링크
     │
     ▼
 PRD 분석 ─── 취소선=폐기, TBD=미확정, 최신 버전 우선
     │
     ▼
 Figma 분석 ─── 화면 프레임 + 플로우차트 + 핸드오프 노트
     │
     ▼
 이해충돌 검토 ─── PRD↔Figma 대조, 충돌/미정의 항목 추출
     │
     ▼
 체크리스트 HTML 생성 ─── 브라우저에서 사용자가 직접 확정
     │ (확정 전까지 다음 단계 진행 안 함)
     ▼
 통합 명세 생성 ─── 확정 결과 기반 단일 문서
     │
     ▼
 TC 생성 (md + html 동시) ─── 근거 기반, 미정의 항목 분리
```

핵심은 "사용자 확정 게이트"입니다. 충돌이 있으면 멈추고 물어봅니다.
AI가 알아서 판단해버리면 결국 사람이 다시 검증해야 하니까요.

---

## 기술적으로 신경 쓴 부분

### 규칙 기반 에이전트 제어

AI한테 "TC 만들어줘"라고 하면 안 됩니다. 규칙 없이 돌리면 추측이 섞이고, 형식이 흔들리고, 디자인 디테일이 들어갑니다.

그래서 Steering 파일 5개로 행동을 제어합니다:

```
qa-workflow.md (전체 흐름 오케스트레이션)
  ├── prd-analysis-rules.md (PRD 분석 규칙)
  ├── figma-analysis-rules.md (Figma 분석 규칙)
  ├── test-case-rules.md (TC 작성 규칙 + 산출물 형식)
  └── language.md (한국어 응답)
```

각 규칙 파일이 하는 일:

| 규칙 파일 | 핵심 제약 |
|----------|----------|
| `qa-workflow.md` | 7단계 순서 강제, 확정 전 TC 생성 금지, 산출물은 파일로 떨구기 |
| `prd-analysis-rules.md` | 취소선=폐기, 회의록은 확정 결론만, Confluence API 자동 수집 |
| `figma-analysis-rules.md` | Handoff 노트 필수 확인, 기존 명세와 충돌 검토 의무화 |
| `test-case-rules.md` | 근거 없으면 TC에 안 넣음, 디자인 디테일 제외, 미정의는 태그 분리 |

### 근거 기반 원칙

TC의 기대 결과에 들어갈 수 있는 것과 없는 것을 명확히 나눴습니다.

```
✅ 근거 인정: PRD 텍스트, 피그마 UI 요소, 플로우차트 화살표, 핸드오프 노트
❌ 근거 불인정: 업계 관행, 유사 서비스 유추, 기술적 구현 가정
```

명세에 없지만 검증이 필요해 보이는 건 `[미정의]` 태그를 붙여서 분리합니다.
"모르는 건 모른다고 표시한다"가 원칙입니다.

### 다중 소스 자동 수집

PRD가 Confluence에 있으면 URL만 주면 API로 가져옵니다.
Figma는 MCP로 메타데이터 + 스크린샷 + 플로우차트를 자동 추출합니다.

수동으로 복붙하는 단계를 없앴습니다.

### 인터랙티브 체크리스트

충돌/미정의 항목을 발견하면 HTML 파일을 생성합니다.
브라우저에서 열어서 "PRD 기준" / "Figma 기준" / "확인 필요"를 클릭하면 됩니다.
로컬 스토리지로 선택 상태가 저장되니까 새로고침해도 날아가지 않습니다.

비개발자(PO, PM)도 브라우저만 열면 확정할 수 있게 만든 겁니다.

---

## 프로젝트 구조

```
qa-tc-agent/
├── .kiro/
│   ├── settings/mcp.json              # Figma MCP 연결 설정
│   └── steering/                      # 에이전트 행동 규칙 (5개)
│       ├── qa-workflow.md
│       ├── prd-analysis-rules.md
│       ├── figma-analysis-rules.md
│       ├── test-case-rules.md
│       └── language.md
├── aidlc-docs/features/               # 피처별 산출물 폴더
│   ├── car-number-promo/              # 4종 세트
│   └── coupon-box/                    # 3종 (체크리스트 이전 작업)
├── examples/coupon-box/               # 출력 형식 템플릿 (품질 벤치마크)
├── webapp/                            # 웹 서비스 확장 (Next.js + FastAPI)
└── portfolio/                         # 이 문서
```

피처 하나당 산출물 4개가 한 세트입니다:

```
aidlc-docs/features/{feature-name}/
├── {feature-name}.md                  ← 통합 명세
├── {feature-name}-checklist.html      ← 이해충돌 체크리스트
├── {feature-name}-test-cases.md       ← TC 마크다운
└── {feature-name}-test-cases.html     ← TC HTML
```

---

## 실행 사례

### 쿠폰함 개선 (coupon-box)

PRD v1.4 (PDF) + Figma 7개 화면을 넣었더니 TC 26건이 나왔습니다.
이 사례로 규칙 파일을 튜닝하고, examples 폴더에 품질 벤치마크로 남겨뒀습니다.

### 차번호 입력 프로모션 (car-number-promo)

Confluence PRD + Figma 2개 파일(기획안 + 최종 디자인)을 분석했습니다.

실행 과정:

1. Confluence API로 PRD 자동 수집
2. Figma MCP로 기획안 분석 → 최종 디자인 파일 별도 존재 확인 → 최종 기준 재분석
3. 이해충돌 10건 발견 → 인터랙티브 체크리스트로 사용자 확정
4. PRD 업데이트 즉시 반영 (상단 네비게이션 변경, 유효성 검증 방식 변경)
5. 최종 TC 32건 생성 (High 16 / Medium 12 / Low 4)

"기획안 피그마"와 "최종 디자인 피그마"가 따로 있는 실제 상황을 처리한 사례입니다.

---

## 사용 기술

| 분류 | 내용 |
|------|------|
| 에이전트 환경 | Kiro IDE (Agent + Steering 시스템) |
| 디자인 연동 | Figma MCP (get_metadata, get_design_context, get_screenshot) |
| 문서 연동 | Confluence REST API |
| 규칙 시스템 | Steering Files 5개 (마크다운 기반 행동 규칙) |
| 웹 확장 | Next.js + FastAPI (webapp/ 폴더) |

---

## 앞으로 하고 싶은 것

- 웹 서비스화 — 브라우저에서 PRD + Figma 넣으면 TC 다운로드 (webapp/ 폴더에 초기 구조 세팅 완료)
- Jira 연동 — TC를 Jira 이슈로 자동 생성
- 회귀 TC 자동 식별 — PRD 업데이트 시 영향받는 TC 자동 마킹
- TC 품질 메트릭 — 근거 커버리지율, 미정의 항목 비율 추적

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
- **웹 서비스 계획**: [webapp-portfolio.md](./webapp-portfolio.md)

# QA TC Generator Agent

PRD(기획문서)와 Figma 디자인을 분석하여 테스트 케이스를 자동 생성하는 Kiro 에이전트입니다.

## 기능

- PRD(PDF) 분석: 화면 정책, 비즈니스 규칙, 에러 정책, API, 이벤트 로그 추출
- Figma 분석: 화면 프레임, 플로우차트, annotations, 핸드오프 노트 확인
- 이해충돌 검토: PRD-피그마 간 충돌/미정의 항목을 체크리스트로 제시
- TC 생성: 근거 기반 테스트 케이스 (md + html 동시 생성)

## 설치

이 레포를 Kiro 워크스페이스로 열면 바로 사용 가능합니다.

## 사전 요구사항

- Kiro IDE 또는 Kiro CLI
- Figma 계정 (MCP 연결을 위한 OAuth 인증)

## 사용 방법

1. Kiro에서 이 워크스페이스를 열기
2. 에이전트 qa-tc-generator를 호출
3. PRD 문서(PDF)를 첨부하고 Figma 링크를 입력
4. 에이전트가 분석 후 이해충돌 체크리스트를 제시
5. 각 항목을 확정하면 통합 명세 + TC가 생성됨

## 워크플로우

입력 수집 (PRD + Figma) → PRD 분석 → Figma 분석 → 이해충돌 검토 (체크리스트) → 통합 명세 생성 → TC 생성 (md + html)

## 출력물

- aidlc-docs/features/{feature}.md — 통합 명세
- aidlc-docs/features/{feature}-test-cases.md — TC (마크다운)
- aidlc-docs/features/{feature}-test-cases.html — TC (브라우저 뷰)

## 프로젝트 구조

qa-tc-agent/
├── .kiro/
│   ├── agents/qa-tc-generator.md
│   ├── settings/mcp.json
│   └── steering/ (5 rule files)
├── aidlc-docs/features/
├── examples/coupon-box/
└── README.md

## TC 작성 핵심 규칙

- 기대 결과는 사용자가 화면에서 인지할 수 있는 요소만 작성
- 디자인 디테일(px, 색상, 좌표 등) 제외
- 근거 없는 추측 금지
- 미정의 항목은 [미정의] 태그로 분리
- 에러 정책이 하나로 커버되면 원인별 TC 분리하지 않음

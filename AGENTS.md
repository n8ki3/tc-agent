# AGENTS

QA TC Generator 에이전트의 공통 진입점이다. 이 저장소는 PRD/Figma/Tech Spec을 분석하여 테스트 케이스를 생성한다. 어떤 AI 도구(Kiro, Codex, Claude Code, Cursor 등)에서 실행되더라도 동일하게 동작하도록, 모든 작업 규칙은 `docs/ai-collaboration/`에 single source of truth로 관리한다.

## 먼저 읽기 (작업 시작 전 필수)

1. [`docs/ai-collaboration/README.md`](./docs/ai-collaboration/README.md) — 먼저 읽기 순서, 작업 라우팅, 문서 맵
2. [`docs/ai-collaboration/policies/qa-workflow.md`](./docs/ai-collaboration/policies/qa-workflow.md) — 전체 작업 흐름
3. 아래 "작업 라우팅"에서 현재 작업 유형에 해당하는 정책 문서

## 작업 라우팅 (작업 유형 → 필독 정책)

작업을 시작하기 전에 해당 정책 문서를 **반드시 직접 열어 읽는다.** 링크만 보고 건너뛰지 않는다.

| 작업 유형 | 필독 정책 문서 (`docs/ai-collaboration/policies/`) |
|-----------|--------------|
| 전체 피처 분석 (TC 생성) | `qa-workflow.md` → `prd-analysis-rules.md` → `figma-analysis-rules.md` → `tech-spec-analysis-rules.md` → `test-case-rules.md` |
| PRD/기획문서 분석 | `prd-analysis-rules.md` |
| Figma 분석 | `figma-analysis-rules.md` |
| Tech Spec 분석 | `tech-spec-analysis-rules.md` |
| 테스트 케이스 작성/수정 | `test-case-rules.md` |
| Google Sheets 시트 추가/갱신 | `gsheet-output-rules.md` |
| Git 커밋/푸시/PR | `git-rules.md` |
| TC 피드백 반영 | `feedback-log.md` + `test-case-rules.md` |

모든 응답은 한국어로 작성한다 ([`language.md`](./docs/ai-collaboration/policies/language.md)).

## 저장소 구조

```
qa-tc-agent/
├── AGENTS.md                       ← 이 문서 (공통 진입점)
├── CLAUDE.md                       ← Claude Code 진입점 (@AGENTS.md import)
├── docs/ai-collaboration/          ← 정책 SSOT
│   ├── README.md                   ← 먼저 읽기 + 작업 라우팅 + 문서 맵
│   ├── policies/                   ← 실제 규칙 (한 벌만 존재)
│   └── tools/                      ← 도구별 진입 방식 (kiro/codex/claude-code)
├── .kiro/
│   ├── settings/                   ← MCP, 크리덴셜
│   └── steering/                   ← Kiro 포인터 (#[[file:]]로 policies 참조)
├── aidlc-docs/features/{피처명}/    ← 생성된 산출물 (통합 명세, TC md/html, meta.json)
├── examples/                       ← 품질 벤치마크 결과물
└── scripts/                        ← Jira Epic 생성 스크립트
```

## 핵심 원칙

- **재발방지 우선** — 누락·오류·충돌이 발견되면 수정으로 끝내지 않는다. 근본 원인을 진단하고, 같은 문제가 다시 생길 수 없도록 구조/프로세스를 고친 뒤 피드백 로그에 남긴다. 단순 수정보다 재발방지가 더 중요하다 (상세: `policies/qa-workflow.md`의 "오류 대응 원칙").
- 정책 규칙의 SSOT는 `docs/ai-collaboration/policies/`다. 규칙 수정은 이 원본에서만 한다.
- 도구별 진입점(`AGENTS.md`, `CLAUDE.md`, `.kiro/steering/*`)에는 규칙을 복제하지 않는다. 참조/라우팅만 둔다.
- 피처별 산출물은 `aidlc-docs/features/{feature-name}/`에 4종 세트(통합 명세, 체크리스트, TC md, TC html) + `meta.json`(Jira Epic/스프레드시트 URL)으로 관리한다.
- 구조가 바뀌면 이 문서와 `docs/ai-collaboration/README.md`를 함께 갱신한다.

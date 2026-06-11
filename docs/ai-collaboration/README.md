# AI Collaboration Guide

이 폴더는 QA TC Generator 에이전트가 **어떤 AI 도구(Kiro, Codex, Claude Code, Cursor 등)에서 실행되더라도 동일하게 동작**하도록 만든 공통 운영 정책의 single source of truth(SSOT)입니다.

실제 작업 규칙은 모두 [`policies/`](./policies/) 아래에 한 벌만 존재하며, 각 도구의 진입점 파일(`AGENTS.md`, `CLAUDE.md`, `.kiro/steering/*`)은 이 문서를 가리키기만 합니다.

## 먼저 읽기 (순서 고정)

작업을 시작하기 전에 아래 순서로 읽는다.

1. 이 문서 (`docs/ai-collaboration/README.md`)
2. **기존 피처 작업을 이어갈 때**: 해당 피처의 `aidlc-docs/features/{feature-name}/meta.json` — `status`/`lastStep`/`pendingItems`로 이전 세션 진행 상태 복구 (세션 핸드오프)
3. [`policies/qa-workflow.md`](./policies/qa-workflow.md) — 전체 작업 흐름 (입력→분석→충돌검토→명세→TC→셀프체크)
4. 작업 유형에 해당하는 정책 문서 (아래 "작업 라우팅" 참조)
5. [`policies/language.md`](./policies/language.md) — 응답 언어 규칙

## 작업 라우팅 (작업 유형 → 필독 정책)

**작업을 시작하기 전에, 해당 행의 정책 문서를 반드시 먼저 읽는다.**

| 작업 유형 | 필독 정책 문서 |
|-----------|--------------|
| 전체 피처 분석 (TC 생성) | `qa-workflow.md` → `prd-analysis-rules.md` → `figma-analysis-rules.md` → `tech-spec-analysis-rules.md` → `test-case-rules.md` |
| PRD/기획문서 분석 | `policies/prd-analysis-rules.md` |
| Figma 분석 | `policies/figma-analysis-rules.md` |
| Tech Spec 분석 | `policies/tech-spec-analysis-rules.md` |
| 테스트 케이스 작성/수정 | `policies/test-case-rules.md` |
| Google Sheets 시트 추가/갱신 | `policies/gsheet-output-rules.md` |
| Git 커밋/푸시/PR | `policies/git-rules.md` |
| TC 피드백 반영 | `policies/feedback-log.md` + `policies/test-case-rules.md` |

## 문서 맵

- [`policies/qa-workflow.md`](./policies/qa-workflow.md) — 분석 워크플로우, Jira 연동, 셀프 체크, 산출물 규칙
- [`policies/prd-analysis-rules.md`](./policies/prd-analysis-rules.md) — PRD 추출 항목, 확정/미확정 판별
- [`policies/figma-analysis-rules.md`](./policies/figma-analysis-rules.md) — 화면/플로우차트/네비게이션 분석
- [`policies/tech-spec-analysis-rules.md`](./policies/tech-spec-analysis-rules.md) — API 분기/에러 코드 → 사전 조건 반영
- [`policies/test-case-rules.md`](./policies/test-case-rules.md) — TC 작성 기준, 용어 통일, 출력 형식
- [`policies/gsheet-output-rules.md`](./policies/gsheet-output-rules.md) — Google Sheets 출력 구조
- [`policies/git-rules.md`](./policies/git-rules.md) — 브랜치/커밋/푸시/Confluence 타임라인
- [`policies/feedback-log.md`](./policies/feedback-log.md) — 피드백 누적 → 규칙 승격
- [`policies/language.md`](./policies/language.md) — 한국어 응답
- [`tools/kiro.md`](./tools/kiro.md) — Kiro 전용 진입 방식
- [`tools/codex.md`](./tools/codex.md) — Codex 전용 진입 방식
- [`tools/claude-code.md`](./tools/claude-code.md) — Claude Code 전용 진입 방식

## 운영 원칙

- 모든 정책은 `policies/` 아래에 **한 벌만** 둔다. 도구별 진입점에 내용을 복제하지 않는다.
- 정책을 수정할 때는 `policies/`의 원본만 고친다. 진입점(`AGENTS.md`, `CLAUDE.md`, `.kiro/steering/*`)은 참조만 하므로 함께 고칠 필요가 없다.
- 새 정책을 추가하면 이 문서의 "작업 라우팅"과 "문서 맵"에 함께 등록한다.
- 도구별 자동 로드 방식이 다르므로(아래 표), 진입점은 각 도구의 강제 로드 메커니즘으로 `policies/`를 끌어온다.

### 도구별 자동 로드 메커니즘

| 도구 | 자동 로드 진입점 | SSOT 연결 방식 |
|------|----------------|---------------|
| Kiro | `.kiro/steering/*.md` (always) | `#[[file:...]]` 참조로 `policies/` 인클루드 |
| Claude Code | `CLAUDE.md` | `@AGENTS.md` import + 본문에서 `docs/` 명시 |
| Codex | `AGENTS.md` | "먼저 읽기" + "작업 라우팅"으로 강하게 유도 |
| Cursor 등 | `AGENTS.md` / 도구별 rules | `AGENTS.md` 라우팅 참조 |

# Claude Code 진입 방식

## 자동 로드

- Claude Code는 저장소 루트의 `CLAUDE.md`를 자동으로 읽는다.
- `CLAUDE.md`는 첫 줄에서 `@AGENTS.md`를 import하여 공통 진입점을 인라인 포함한다.
- `AGENTS.md`의 "작업 라우팅"을 따라 `docs/ai-collaboration/policies/`의 정책 문서를 읽는다.

## 작업 시작 절차

1. `CLAUDE.md` (→ `@AGENTS.md`)를 읽는다.
2. `docs/ai-collaboration/README.md`의 "작업 라우팅"에서 작업 유형에 맞는 정책 문서를 연다.
3. 해당 정책 문서를 읽은 뒤 작업을 시작한다.

## 주의

- 정책 SSOT는 `docs/ai-collaboration/policies/`이다. `CLAUDE.md`에는 Claude 전용 보강 규칙만 둔다.
- 규칙 변경은 `policies/` 원본에서만 한다.

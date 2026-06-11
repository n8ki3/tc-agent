# Codex 진입 방식

## 자동 로드

- Codex는 저장소 루트의 `AGENTS.md`를 진입점으로 읽는다.
- `AGENTS.md`는 "먼저 읽기" 순서와 "작업 라우팅" 표를 담고 있으며, 작업 유형에 맞는 `docs/ai-collaboration/policies/` 문서를 읽도록 강하게 유도한다.

## 작업 시작 절차

1. 루트 `AGENTS.md`를 읽는다.
2. `docs/ai-collaboration/README.md`의 "작업 라우팅"에서 현재 작업 유형에 해당하는 정책 문서를 확인한다.
3. 해당 정책 문서를 **실제로 열어 읽은 뒤** 작업을 시작한다. (라우팅에 명시된 문서를 건너뛰지 않는다)

## 주의

- Codex는 import 강제 메커니즘이 없으므로, 라우팅에 명시된 정책 문서를 반드시 직접 읽어야 한다.
- 정책 내용은 `docs/ai-collaboration/policies/`가 SSOT이다. `AGENTS.md`에 규칙을 복제하지 않는다.

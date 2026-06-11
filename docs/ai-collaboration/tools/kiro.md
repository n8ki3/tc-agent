# Kiro 진입 방식

## 자동 로드

- Kiro는 `.kiro/steering/*.md`를 항상(always) 컨텍스트에 로드한다.
- 각 steering 파일은 얇은 **포인터**이며, `#[[file:../../docs/ai-collaboration/policies/{name}.md]]` 참조로 SSOT 원본을 함께 로드한다.
- 따라서 실제 규칙 내용은 `docs/ai-collaboration/policies/`에 있고, Kiro는 포인터를 통해 빠짐없이 읽는다.

## 설정 파일

- MCP: `.kiro/settings/mcp.json` (Figma, Proxyman)
- Google Sheets 크리덴셜: `.kiro/settings/finda-stg-gspread.json` (gitignore 대상)

## 규칙 수정 시

- **규칙 내용은 `docs/ai-collaboration/policies/`의 원본만 수정한다.**
- `.kiro/steering/*.md` 포인터는 경로만 가리키므로 건드리지 않는다.
- 새 정책 파일을 추가하면 `.kiro/steering/`에도 대응 포인터를 만들고, `docs/ai-collaboration/README.md`의 라우팅/문서 맵을 갱신한다.

## 비고

- Kiro 사용은 한시적이며, 정책 SSOT가 `docs/`에 있으므로 다른 도구로 전환해도 규칙은 그대로 유지된다.

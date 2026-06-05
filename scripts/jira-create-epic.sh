#!/bin/bash
# Jira QA Epic 생성 + QA요청 티켓 Parent 연결
# 사용법: ./scripts/jira-create-epic.sh <QA요청_티켓_KEY> <Epic_Summary> <디자인닥_URL> <피그마_URL> [Tech_Spec_URL...]
#
# 예시:
#   ./scripts/jira-create-epic.sh FQA-2214 "[QA] 마수동 유도 인앱 바텀싯 3차" \
#     "https://findainc.atlassian.net/wiki/spaces/MD/pages/5355995455/26-2Q+3" \
#     "https://www.figma.com/design/F5Hdwh..."

set -e

# .env 파일에서 인증 정보 로드
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"
source "$PROJECT_ROOT/.env"

AUTH="$CONFLUENCE_EMAIL:$CONFLUENCE_TOKEN"
BASE_URL="$CONFLUENCE_BASE_URL"

QA_REQUEST_KEY="$1"
EPIC_SUMMARY="$2"
DESIGN_DOC_URL="$3"
FIGMA_URL="$4"
shift 4
TECH_SPEC_URLS=("$@")

if [ -z "$QA_REQUEST_KEY" ] || [ -z "$EPIC_SUMMARY" ]; then
  echo "❌ 사용법: $0 <QA요청KEY> <Epic_Summary> [디자인닥URL] [피그마URL] [TechSpecURL...]"
  exit 1
fi

echo "📋 Jira QA Epic 생성 시작..."
echo "   QA 요청: $QA_REQUEST_KEY"
echo "   Epic 제목: $EPIC_SUMMARY"

# Description 구성 (ADF 포맷)
DESC_CONTENT='['
DESC_CONTENT+='{"type":"paragraph","content":[{"type":"text","text":"QA 요청 티켓: ","marks":[{"type":"strong"}]},{"type":"inlineCard","attrs":{"url":"'"$BASE_URL"'/browse/'"$QA_REQUEST_KEY"'"}},{"type":"text","text":" "}]}'

if [ -n "$DESIGN_DOC_URL" ]; then
  DESC_CONTENT+=',{"type":"paragraph","content":[{"type":"text","text":"디자인닥: ","marks":[{"type":"strong"}]},{"type":"inlineCard","attrs":{"url":"'"$DESIGN_DOC_URL"'"}},{"type":"text","text":" "}]}'
fi

if [ -n "$FIGMA_URL" ]; then
  DESC_CONTENT+=',{"type":"paragraph","content":[{"type":"text","text":"피그마: ","marks":[{"type":"strong"}]},{"type":"inlineCard","attrs":{"url":"'"$FIGMA_URL"'"}},{"type":"text","text":" "}]}'
fi

for TS_URL in "${TECH_SPEC_URLS[@]}"; do
  if [ -n "$TS_URL" ]; then
    DESC_CONTENT+=',{"type":"paragraph","content":[{"type":"text","text":"Tech Spec: ","marks":[{"type":"strong"}]},{"type":"inlineCard","attrs":{"url":"'"$TS_URL"'"}},{"type":"text","text":" "}]}'
  fi
done

DESC_CONTENT+=']'

# 1. Epic 생성
echo ""
echo "1️⃣ Epic 생성 중..."
EPIC_RESPONSE=$(curl -s -X POST -u "$AUTH" \
  -H "Content-Type: application/json" \
  "$BASE_URL/rest/api/3/issue" \
  -d '{
    "fields": {
      "project": {"id": "11206"},
      "issuetype": {"id": "10004"},
      "summary": "'"$EPIC_SUMMARY"'",
      "description": {
        "version": 1,
        "type": "doc",
        "content": '"$DESC_CONTENT"'
      }
    }
  }')

EPIC_KEY=$(echo "$EPIC_RESPONSE" | python3 -c "import json,sys; d=json.load(sys.stdin); print(d.get('key',''))" 2>/dev/null)

if [ -z "$EPIC_KEY" ]; then
  echo "❌ Epic 생성 실패:"
  echo "$EPIC_RESPONSE" | python3 -m json.tool 2>/dev/null || echo "$EPIC_RESPONSE"
  exit 1
fi

echo "   ✅ Epic 생성 완료: $EPIC_KEY"
echo "   🔗 $BASE_URL/browse/$EPIC_KEY"

# 2. QA요청 티켓 Parent 연결
echo ""
echo "2️⃣ $QA_REQUEST_KEY → $EPIC_KEY Parent 연결 중..."
HTTP_STATUS=$(curl -s -o /dev/null -w "%{http_code}" -X PUT -u "$AUTH" \
  -H "Content-Type: application/json" \
  "$BASE_URL/rest/api/3/issue/$QA_REQUEST_KEY" \
  -d '{"fields":{"parent":{"key":"'"$EPIC_KEY"'"}}}')

if [ "$HTTP_STATUS" = "204" ]; then
  echo "   ✅ Parent 연결 완료"
else
  echo "   ⚠️ Parent 연결 HTTP $HTTP_STATUS (이미 연결되어 있을 수 있음)"
fi

echo ""
echo "✅ 완료!"
echo "   Epic: $BASE_URL/browse/$EPIC_KEY"
echo "   구조: $EPIC_KEY (Epic) ← $QA_REQUEST_KEY (QA요청)"

# 결과를 환경변수 파일로 출력 (후속 스크립트에서 사용)
echo "$EPIC_KEY" > "$PROJECT_ROOT/.last_epic_key"

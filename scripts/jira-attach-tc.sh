#!/bin/bash
# Jira Epic에 TC HTML 첨부
# 사용법: ./scripts/jira-attach-tc.sh <EPIC_KEY> <TC_HTML_파일경로>
#
# 예시:
#   ./scripts/jira-attach-tc.sh FQA-2215 aidlc-docs/features/msd-inapp-bottomsheet/msd-inapp-bottomsheet-test-cases.html

set -e

# .env 파일에서 인증 정보 로드
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"
source "$PROJECT_ROOT/.env"

AUTH="$CONFLUENCE_EMAIL:$CONFLUENCE_TOKEN"
BASE_URL="$CONFLUENCE_BASE_URL"

EPIC_KEY="$1"
TC_FILE="$2"

# EPIC_KEY가 없으면 .last_epic_key에서 읽기
if [ -z "$EPIC_KEY" ]; then
  if [ -f "$PROJECT_ROOT/.last_epic_key" ]; then
    EPIC_KEY=$(cat "$PROJECT_ROOT/.last_epic_key")
    echo "📌 .last_epic_key에서 읽음: $EPIC_KEY"
  else
    echo "❌ 사용법: $0 <EPIC_KEY> <TC_HTML_파일경로>"
    exit 1
  fi
fi

if [ -z "$TC_FILE" ]; then
  echo "❌ TC HTML 파일 경로를 지정해주세요."
  echo "   사용법: $0 <EPIC_KEY> <TC_HTML_파일경로>"
  exit 1
fi

# 상대경로 → 절대경로
if [[ "$TC_FILE" != /* ]]; then
  TC_FILE="$PROJECT_ROOT/$TC_FILE"
fi

if [ ! -f "$TC_FILE" ]; then
  echo "❌ 파일 없음: $TC_FILE"
  exit 1
fi

echo "📎 TC HTML 첨부 시작..."
echo "   Epic: $EPIC_KEY"
echo "   파일: $(basename "$TC_FILE")"

RESPONSE=$(curl -s -X POST -u "$AUTH" \
  -H "X-Atlassian-Token: no-check" \
  -F "file=@$TC_FILE" \
  "$BASE_URL/rest/api/3/issue/$EPIC_KEY/attachments")

FILENAME=$(echo "$RESPONSE" | python3 -c "import json,sys; d=json.load(sys.stdin); print(d[0]['filename'] if isinstance(d,list) and len(d)>0 else '')" 2>/dev/null)

if [ -n "$FILENAME" ]; then
  FILESIZE=$(echo "$RESPONSE" | python3 -c "import json,sys; d=json.load(sys.stdin); print(d[0]['size'])" 2>/dev/null)
  echo "   ✅ 첨부 완료: $FILENAME ($FILESIZE bytes)"
else
  echo "   ❌ 첨부 실패:"
  echo "$RESPONSE" | python3 -m json.tool 2>/dev/null || echo "$RESPONSE"
  exit 1
fi

echo ""
echo "✅ 완료! $BASE_URL/browse/$EPIC_KEY 에서 확인하세요."

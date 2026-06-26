"""
실험 2: Figma REST API — 노드 구조 + 텍스트 추출 테스트

사용법:
  python3 experiments/02_figma_api.py <FIGMA_TOKEN> <FIGMA_URL>

예시:
  python3 experiments/02_figma_api.py figd_xxxx "https://www.figma.com/design/ABC123/파일명?node-id=726-8226"

토큰 발급:
  Figma → Settings → Personal Access Tokens → Generate new token
"""

import sys
import json
import re
from urllib.parse import urlparse, parse_qs

try:
    import httpx
except ImportError:
    print("httpx가 필요합니다: pip3 install httpx")
    sys.exit(1)


def parse_figma_url(url: str) -> tuple[str, str]:
    """Figma URL에서 file_key와 node_id 추출"""
    # https://www.figma.com/design/FILE_KEY/파일명?node-id=123-456
    # https://www.figma.com/file/FILE_KEY/파일명?node-id=123-456

    parsed = urlparse(url)
    path_parts = parsed.path.strip("/").split("/")

    file_key = None
    node_id = None

    # file_key 추출
    if "design" in path_parts:
        idx = path_parts.index("design")
        if idx + 1 < len(path_parts):
            file_key = path_parts[idx + 1]
    elif "file" in path_parts:
        idx = path_parts.index("file")
        if idx + 1 < len(path_parts):
            file_key = path_parts[idx + 1]

    # node_id 추출
    query = parse_qs(parsed.query)
    if "node-id" in query:
        node_id = query["node-id"][0].replace("-", ":")

    return file_key, node_id


class FigmaClient:
    def __init__(self, token: str):
        self.token = token
        self.base_url = "https://api.figma.com/v1"
        self.headers = {"X-Figma-Token": token}

    def get_file(self, file_key: str, node_id: str = None) -> dict:
        """파일 또는 특정 노드 정보 조회"""
        if node_id:
            url = f"{self.base_url}/files/{file_key}/nodes?ids={node_id}"
        else:
            url = f"{self.base_url}/files/{file_key}"

        with httpx.Client(timeout=30) as client:
            resp = client.get(url, headers=self.headers)
            resp.raise_for_status()
            return resp.json()

    def get_images(self, file_key: str, node_ids: list[str], scale: float = 1) -> dict:
        """노드 이미지(스크린샷) URL 조회"""
        ids = ",".join(node_ids)
        url = f"{self.base_url}/images/{file_key}?ids={ids}&scale={scale}&format=png"

        with httpx.Client(timeout=30) as client:
            resp = client.get(url, headers=self.headers)
            resp.raise_for_status()
            return resp.json()

    def extract_texts(self, node: dict, depth: int = 0) -> list[dict]:
        """재귀적으로 모든 텍스트 노드 추출"""
        texts = []

        if node.get("type") == "TEXT":
            texts.append({
                "name": node.get("name", ""),
                "text": node.get("characters", ""),
                "depth": depth,
                "style": {
                    "fontSize": node.get("style", {}).get("fontSize"),
                    "fontWeight": node.get("style", {}).get("fontWeight"),
                    "textDecoration": node.get("style", {}).get("textDecoration"),
                },
            })

        for child in node.get("children", []):
            texts.extend(self.extract_texts(child, depth + 1))

        return texts

    def extract_structure(self, node: dict, depth: int = 0, max_depth: int = 3) -> list[dict]:
        """노드 트리 구조 추출 (depth 제한)"""
        structure = []

        structure.append({
            "depth": depth,
            "type": node.get("type"),
            "name": node.get("name", ""),
            "id": node.get("id", ""),
            "children_count": len(node.get("children", [])),
        })

        if depth < max_depth:
            for child in node.get("children", []):
                structure.extend(self.extract_structure(child, depth + 1, max_depth))

        return structure

    def find_flowchart_nodes(self, node: dict) -> list[dict]:
        """플로우차트/핸드오프 관련 노드 찾기"""
        keywords = ["flowchart", "flow", "handoff", "interaction", "sub parts", "annotation"]
        found = []

        name_lower = node.get("name", "").lower()
        if any(kw in name_lower for kw in keywords):
            found.append({
                "id": node.get("id"),
                "name": node.get("name"),
                "type": node.get("type"),
            })

        for child in node.get("children", []):
            found.extend(self.find_flowchart_nodes(child))

        return found


def main():
    if len(sys.argv) < 3:
        print("사용법: python3 experiments/02_figma_api.py <FIGMA_TOKEN> <FIGMA_URL>")
        print()
        print("토큰 발급 방법:")
        print("  1. https://www.figma.com/settings 접속")
        print("  2. 'Personal Access Tokens' 섹션")
        print("  3. 'Generate new token' 클릭")
        print()
        print("URL 예시:")
        print("  https://www.figma.com/design/ABC123/파일명?node-id=726-8226")
        sys.exit(1)

    token = sys.argv[1]
    figma_url = sys.argv[2]

    # URL 파싱
    file_key, node_id = parse_figma_url(figma_url)
    print(f"\n{'='*60}")
    print(f"Figma API 실험")
    print(f"{'='*60}")
    print(f"  File Key: {file_key}")
    print(f"  Node ID:  {node_id}")

    if not file_key:
        print("\n❌ URL에서 file_key를 추출할 수 없습니다.")
        sys.exit(1)

    client = FigmaClient(token)

    # 1. 노드 정보 조회
    print(f"\n[1] 노드 정보 조회")
    print("-" * 40)
    try:
        data = client.get_file(file_key, node_id)
        print("  ✅ API 호출 성공")

        # nodes 구조에서 실제 노드 추출
        if "nodes" in data:
            node_data = list(data["nodes"].values())[0]
            root_node = node_data.get("document", {})
        else:
            root_node = data.get("document", {})

        print(f"  루트 노드: {root_node.get('name', 'N/A')} ({root_node.get('type', 'N/A')})")

    except httpx.HTTPStatusError as e:
        print(f"  ❌ API 에러: {e.response.status_code}")
        print(f"     {e.response.text[:200]}")
        sys.exit(1)
    except Exception as e:
        print(f"  ❌ 연결 에러: {e}")
        sys.exit(1)

    # 2. 구조 추출
    print(f"\n[2] 노드 트리 구조 (depth 3)")
    print("-" * 40)
    structure = client.extract_structure(root_node, max_depth=3)
    for item in structure[:30]:
        indent = "  " * (item["depth"] + 1)
        children = f" ({item['children_count']} children)" if item["children_count"] > 0 else ""
        print(f"{indent}[{item['type']}] {item['name']}{children}")

    if len(structure) > 30:
        print(f"  ... 외 {len(structure) - 30}개 노드")

    # 3. 텍스트 추출
    print(f"\n[3] 텍스트 노드 추출")
    print("-" * 40)
    texts = client.extract_texts(root_node)
    print(f"  텍스트 노드: {len(texts)}개")

    for item in texts[:20]:
        text_preview = item["text"][:60].replace("\n", " ")
        decoration = ""
        if item["style"].get("textDecoration") == "STRIKETHROUGH":
            decoration = " [취소선]"
        weight = ""
        if item["style"].get("fontWeight") and item["style"]["fontWeight"] >= 700:
            weight = " [볼드]"
        print(f"    {item['name']}: \"{text_preview}\"{decoration}{weight}")

    # 4. 플로우차트/핸드오프 노드 찾기
    print(f"\n[4] 플로우차트/핸드오프 노드 탐색")
    print("-" * 40)
    flow_nodes = client.find_flowchart_nodes(root_node)
    print(f"  발견: {len(flow_nodes)}개")
    for item in flow_nodes[:10]:
        print(f"    [{item['type']}] {item['name']} (id: {item['id']})")

    # 5. 이미지(스크린샷) URL 조회
    if node_id:
        print(f"\n[5] 스크린샷 URL 조회")
        print("-" * 40)
        try:
            images = client.get_images(file_key, [node_id])
            image_urls = images.get("images", {})
            for nid, url in image_urls.items():
                if url:
                    print(f"  ✅ 스크린샷 URL 생성됨")
                    print(f"     {url[:100]}...")
                else:
                    print(f"  ⚠️  이미지 생성 실패 (노드가 비어있거나 렌더링 불가)")
        except Exception as e:
            print(f"  ❌ 이미지 조회 실패: {e}")

    # 결과 저장
    output = {
        "file_key": file_key,
        "node_id": node_id,
        "structure_count": len(structure),
        "text_count": len(texts),
        "flow_nodes_count": len(flow_nodes),
        "structure_sample": structure[:20],
        "texts_sample": texts[:20],
        "flow_nodes": flow_nodes,
    }
    output_path = "experiments/02_figma_result.json"
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(output, f, ensure_ascii=False, indent=2)
    print(f"\n✅ 상세 결과 저장: {output_path}")

    # 요약
    print(f"\n{'='*60}")
    print("실험 요약")
    print(f"{'='*60}")
    print(f"  노드 구조: {len(structure)}개 노드 탐색됨")
    print(f"  텍스트: {len(texts)}개 추출됨")
    print(f"  플로우차트 노드: {len(flow_nodes)}개 발견")

    # 취소선 텍스트 확인
    strikethrough_texts = [t for t in texts if t["style"].get("textDecoration") == "STRIKETHROUGH"]
    if strikethrough_texts:
        print(f"\n  🎯 취소선 텍스트 발견: {len(strikethrough_texts)}개")
        for t in strikethrough_texts:
            print(f"     \"{t['text'][:50]}\"")
    else:
        print(f"\n  ℹ️  취소선 텍스트 없음 (이 노드 범위 내)")


if __name__ == "__main__":
    main()

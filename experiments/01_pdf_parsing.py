"""
실험 1: PDF 파싱 — 취소선, 볼드, 표 추출 테스트

사용법:
  python3 experiments/01_pdf_parsing.py <PDF 파일 경로>

예시:
  python3 experiments/01_pdf_parsing.py ~/Downloads/coupon-box-prd.pdf
"""

import sys
import json
import fitz  # PyMuPDF
import pdfplumber


def extract_with_pymupdf(pdf_path: str) -> dict:
    """PyMuPDF로 텍스트 + 서식 정보 추출"""
    doc = fitz.open(pdf_path)
    result = {
        "total_pages": len(doc),
        "strikethrough_texts": [],  # 취소선 텍스트
        "bold_texts": [],           # 볼드 텍스트
        "all_texts_sample": [],     # 전체 텍스트 샘플 (첫 3페이지)
    }

    for page_num, page in enumerate(doc):
        text_dict = page.get_text("dict")

        for block in text_dict.get("blocks", []):
            if block["type"] != 0:  # 텍스트 블록만
                continue

            for line in block.get("lines", []):
                for span in line.get("spans", []):
                    text = span["text"].strip()
                    if not text:
                        continue

                    flags = span.get("flags", 0)
                    font = span.get("font", "")
                    size = span.get("size", 0)

                    # 취소선 감지 (flags bit)
                    # PyMuPDF flags: superscript=1, italic=2, serifed=4, monospaced=8, bold=16
                    is_bold = bool(flags & 16) or "Bold" in font or "bold" in font

                    # 취소선은 PyMuPDF에서 직접 감지가 어려울 수 있음
                    # 대안: 텍스트 위에 line annotation 확인
                    if is_bold:
                        result["bold_texts"].append({
                            "page": page_num + 1,
                            "text": text[:100],
                            "font": font,
                        })

                    if page_num < 3:
                        result["all_texts_sample"].append({
                            "page": page_num + 1,
                            "text": text[:80],
                            "flags": flags,
                            "font": font,
                            "size": round(size, 1),
                        })

    # 취소선 감지: line annotations 확인
    for page_num, page in enumerate(doc):
        # 방법 1: 텍스트 위의 선(line) 그래픽 확인
        drawings = page.get_drawings()
        for drawing in drawings:
            if drawing.get("type") == "l":  # line
                # 수평선이면서 텍스트 영역과 겹치면 취소선일 가능성
                pass

        # 방법 2: Strikeout annotation 확인
        for annot in page.annots() or []:
            if annot.type[0] == 6:  # Strikeout annotation
                result["strikethrough_texts"].append({
                    "page": page_num + 1,
                    "text": annot.info.get("content", "")[:100],
                    "rect": list(annot.rect),
                })

    doc.close()
    return result


def extract_tables_with_pdfplumber(pdf_path: str) -> dict:
    """pdfplumber로 표 추출"""
    result = {
        "tables_found": 0,
        "tables": [],
    }

    with pdfplumber.open(pdf_path) as pdf:
        for page_num, page in enumerate(pdf.pages):
            tables = page.extract_tables()
            for table_idx, table in enumerate(tables):
                result["tables_found"] += 1
                # 첫 5개 표만 샘플로 저장
                if result["tables_found"] <= 5:
                    result["tables"].append({
                        "page": page_num + 1,
                        "rows": len(table),
                        "cols": len(table[0]) if table else 0,
                        "header": table[0] if table else [],
                        "sample_rows": table[1:4] if len(table) > 1 else [],
                    })

    return result


def extract_strikethrough_via_redaction(pdf_path: str) -> list:
    """
    취소선 텍스트를 찾는 대안 방법:
    PDF의 텍스트 렌더링 모드와 그래픽 오버레이를 분석
    """
    doc = fitz.open(pdf_path)
    strikethrough_candidates = []

    for page_num, page in enumerate(doc):
        # 텍스트 블록의 위치 정보 수집
        text_blocks = []
        text_dict = page.get_text("dict")
        for block in text_dict.get("blocks", []):
            if block["type"] != 0:
                continue
            for line in block.get("lines", []):
                for span in line.get("spans", []):
                    if span["text"].strip():
                        text_blocks.append({
                            "text": span["text"],
                            "bbox": span["bbox"],  # (x0, y0, x1, y1)
                            "origin": span["origin"],
                            "size": span["size"],
                        })

        # 수평선(drawings) 중 텍스트 중앙을 가로지르는 것 찾기
        drawings = page.get_drawings()
        for path in drawings:
            for item in path.get("items", []):
                if item[0] == "l":  # line
                    p1, p2 = item[1], item[2]
                    # 수평선인지 확인 (y 좌표 차이가 작음)
                    if abs(p1.y - p2.y) < 2:
                        line_y = p1.y
                        line_x0 = min(p1.x, p2.x)
                        line_x1 = max(p1.x, p2.x)

                        # 이 선이 텍스트 중앙을 지나는지 확인
                        for tb in text_blocks:
                            text_mid_y = (tb["bbox"][1] + tb["bbox"][3]) / 2
                            if (abs(line_y - text_mid_y) < tb["size"] * 0.3 and
                                line_x0 <= tb["bbox"][0] and
                                line_x1 >= tb["bbox"][2] - 5):
                                strikethrough_candidates.append({
                                    "page": page_num + 1,
                                    "text": tb["text"][:100],
                                })

    doc.close()
    return strikethrough_candidates


def main():
    if len(sys.argv) < 2:
        print("사용법: python3 experiments/01_pdf_parsing.py <PDF 파일 경로>")
        print()
        print("테스트할 PDF가 없으면 샘플 PDF를 생성합니다...")
        create_sample_pdf()
        pdf_path = "experiments/sample_prd.pdf"
    else:
        pdf_path = sys.argv[1]

    print(f"\n{'='*60}")
    print(f"PDF 파싱 실험: {pdf_path}")
    print(f"{'='*60}")

    # 1. PyMuPDF 텍스트 + 서식 추출
    print("\n[1] PyMuPDF — 텍스트 + 서식 추출")
    print("-" * 40)
    pymupdf_result = extract_with_pymupdf(pdf_path)
    print(f"  총 페이지: {pymupdf_result['total_pages']}")
    print(f"  볼드 텍스트: {len(pymupdf_result['bold_texts'])}개")
    print(f"  취소선 (annotation): {len(pymupdf_result['strikethrough_texts'])}개")

    if pymupdf_result["bold_texts"]:
        print("\n  [볼드 텍스트 샘플]")
        for item in pymupdf_result["bold_texts"][:5]:
            print(f"    p.{item['page']}: {item['text']}")

    if pymupdf_result["strikethrough_texts"]:
        print("\n  [취소선 텍스트]")
        for item in pymupdf_result["strikethrough_texts"][:5]:
            print(f"    p.{item['page']}: {item['text']}")

    # 2. 취소선 대안 감지
    print("\n[2] 취소선 감지 (그래픽 오버레이 분석)")
    print("-" * 40)
    strikethrough = extract_strikethrough_via_redaction(pdf_path)
    print(f"  취소선 후보: {len(strikethrough)}개")
    for item in strikethrough[:10]:
        print(f"    p.{item['page']}: {item['text']}")

    # 3. pdfplumber 표 추출
    print("\n[3] pdfplumber — 표 추출")
    print("-" * 40)
    table_result = extract_tables_with_pdfplumber(pdf_path)
    print(f"  발견된 표: {table_result['tables_found']}개")
    for table in table_result["tables"][:3]:
        print(f"\n  [표 p.{table['page']}] {table['rows']}행 × {table['cols']}열")
        print(f"    헤더: {table['header']}")
        for row in table["sample_rows"][:2]:
            print(f"    데이터: {row}")

    # 4. 전체 텍스트 샘플
    print("\n[4] 전체 텍스트 샘플 (첫 3페이지)")
    print("-" * 40)
    for item in pymupdf_result["all_texts_sample"][:20]:
        flag_str = f"[B]" if item["flags"] & 16 else "   "
        print(f"  {flag_str} p.{item['page']} ({item['size']}pt): {item['text']}")

    # 결과 JSON 저장
    output = {
        "pymupdf": pymupdf_result,
        "strikethrough_candidates": strikethrough,
        "tables": table_result,
    }
    output_path = "experiments/01_pdf_result.json"
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(output, f, ensure_ascii=False, indent=2)
    print(f"\n✅ 상세 결과 저장: {output_path}")


def create_sample_pdf():
    """테스트용 샘플 PDF 생성"""
    doc = fitz.open()
    page = doc.new_page()

    # 일반 텍스트
    page.insert_text((72, 72), "쿠폰함 개선 PRD v1.4", fontsize=18,
                     fontname="helv")

    # 볼드 텍스트
    page.insert_text((72, 120), "확정 정책: 최대 혜택 쿠폰 자동 선택",
                     fontsize=12, fontname="helv")

    # 취소선 시뮬레이션 (텍스트 + 위에 선 그리기)
    text_y = 160
    page.insert_text((72, text_y), "할인율형 쿠폰 (0.5% 할인)", fontsize=12,
                     fontname="helv")
    # 텍스트 중앙에 선 그리기 (취소선 효과)
    page.draw_line((72, text_y - 4), (280, text_y - 4),
                   color=(0, 0, 0), width=0.8)

    # TBD 텍스트
    page.insert_text((72, 200), "[TBD] 스낵바 자동 사라짐 시간",
                     fontsize=12, fontname="helv")

    # SCOPE OUT
    page.insert_text((72, 240), "[SCOPE OUT] best_coupon 이벤트 프로퍼티",
                     fontsize=12, fontname="helv")

    doc.save("experiments/sample_prd.pdf")
    doc.close()
    print("  → 샘플 PDF 생성 완료: experiments/sample_prd.pdf")


if __name__ == "__main__":
    main()

# 실험 모듈

웹 애플리케이션 전환을 위한 핵심 기술 검증 실험입니다.

## 실험 목록

### 01. PDF 파싱 (`01_pdf_parsing.py`)

PRD PDF에서 취소선, 볼드, 표를 추출할 수 있는지 검증합니다.

```bash
# 샘플 PDF로 테스트 (PDF 없어도 실행 가능)
python3 experiments/01_pdf_parsing.py

# 실제 PRD PDF로 테스트
python3 experiments/01_pdf_parsing.py ~/Downloads/your-prd.pdf
```

**검증 항목:**
- [x] 텍스트 추출 (PyMuPDF)
- [x] 취소선 감지 (그래픽 오버레이 분석)
- [x] 볼드 텍스트 감지 (font flags)
- [x] 표 추출 (pdfplumber)
- [ ] 실제 PRD PDF로 정확도 확인 (PDF 필요)

---

### 02. Figma REST API (`02_figma_api.py`)

Figma Personal Access Token으로 노드 구조와 텍스트를 추출할 수 있는지 검증합니다.

```bash
python3 experiments/02_figma_api.py <FIGMA_TOKEN> "<FIGMA_URL>"
```

**토큰 발급:**
1. https://www.figma.com/settings 접속
2. 'Personal Access Tokens' 섹션
3. 'Generate new token' 클릭

**검증 항목:**
- [ ] API 인증 성공
- [ ] 노드 트리 구조 조회
- [ ] 텍스트 노드 추출
- [ ] 취소선(textDecoration: STRIKETHROUGH) 감지
- [ ] 플로우차트/핸드오프 노드 탐색
- [ ] 스크린샷 URL 생성

---

## 의존성

```bash
pip3 install pymupdf pdfplumber httpx
```

## 결과 파일

실험 실행 후 JSON 결과가 저장됩니다:
- `01_pdf_result.json` — PDF 파싱 결과
- `02_figma_result.json` — Figma API 결과

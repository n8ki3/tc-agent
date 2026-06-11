# Google Sheets TC 출력 규칙

## 개요

TC 확정 후 Google Sheets에도 시트를 추가하여 QA 팀이 브라우저에서 직접 수행 결과를 기록할 수 있게 한다.
TC HTML은 로컬 산출물로만 생성하며(Jira에는 첨부하지 않음), 스프레드시트는 팀 공유 및 차수별 이력 관리 용도로 사용한다. Jira Epic에는 스프레드시트 링크만 추가한다.

## 대상 스프레드시트

- QA Epic 티켓의 Description 또는 기존 차수 체크리스트에서 Google Sheets URL을 확인한다.
- 동일 피처의 이전 차수 시트가 있는 스프레드시트에 새 시트를 추가한다.
- 새 피처이거나 기존 시트가 없으면 사용자에게 시트 URL을 요청한다.

## 인증

- `.kiro/settings/finda-stg-gspread.json` Service Account 크리덴셜 사용
- Scopes: `spreadsheets`, `drive`
- Service Account 이메일(`gspread@finda-stg.iam.gserviceaccount.com`)이 스프레드시트에 **편집자** 권한으로 초대되어 있어야 한다.

## 시트 구조

### 시트명

- `{차수}차` (예: `1차 통합`, `3차`)
- 기존 차수와 구분 가능하게 명명

### 열 구조 (11열, A~K)

HTML TC와 동일한 컬럼:

| 열 | 내용 |
|----|------|
| A | TC_ID |
| B | Category1 |
| C | Category2 |
| D | Category3 |
| E | Level |
| F | pre-Condition |
| G | Test Procedure |
| H | Expected Result |
| I | Android (드롭다운) |
| J | iOS (드롭다운) |
| K | Comment |

### 상단 통계 (1~5행)

| 행 | 내용 |
|----|------|
| 1 | 제목 (피처명 + 차수) |
| 2 | 빈 행 |
| 3 | 통계 라벨: `전체 TC` / `High` / `Medium` / `Low` / (빈) / `실행률` / `패스율` / `Pass` / `Fail` / `N/T` / `N/A` |
| 4 | 통계 값: 고정값 4개 + 수식 7개 |
| 5 | 빈 행 |

### 통계 수식 (4행)

| 셀 | 수식 |
|----|------|
| A4 | 전체 TC 수 (고정값) |
| B4 | High 수 (고정값) |
| C4 | Medium 수 (고정값) |
| D4 | Low 수 (고정값) |
| F4 | `=IF(A4>0,ROUND((H4+I4)/A4*100,1)&"%","0%")` |
| G4 | `=IF((H4+I4)>0,ROUND(H4/(H4+I4)*100,1)&"%","0%")` |
| H4 | `=COUNTIF(I{start}:I{end},"Pass")+COUNTIF(J{start}:J{end},"Pass")` |
| I4 | `=COUNTIF(I{start}:I{end},"Fail")+COUNTIF(J{start}:J{end},"Fail")` |
| J4 | `=COUNTIF(I{start}:I{end},"N/T")+COUNTIF(J{start}:J{end},"N/T")` |
| K4 | `=COUNTIF(I{start}:I{end},"N/A")+COUNTIF(J{start}:J{end},"N/A")` |

- `{start}`: TC 데이터 시작 행 (헤더 다음 행)
- `{end}`: TC 데이터 마지막 행
- 수식은 `value_input_option='USER_ENTERED'`로 입력해야 수식으로 인식됨

### 데이터 시작 (6행~)

| 행 | 내용 |
|----|------|
| 6 | 헤더 행 (TC_ID / Category1 / ... / Comment) |
| 7~ | TC 데이터 |

## 드롭다운 설정

Android(I열)과 iOS(J열)에 데이터 유효성 검사(Data Validation)를 설정한다:

```python
{
    'setDataValidation': {
        'range': {
            'sheetId': ws.id,
            'startRowIndex': tc_start - 1,  # 0-based
            'endRowIndex': tc_end,
            'startColumnIndex': 8,   # I열
            'endColumnIndex': 10,    # J열까지
        },
        'rule': {
            'condition': {
                'type': 'ONE_OF_LIST',
                'values': [
                    {'userEnteredValue': 'Pass'},
                    {'userEnteredValue': 'Fail'},
                    {'userEnteredValue': 'N/T'},
                    {'userEnteredValue': 'N/A'},
                ]
            },
            'showCustomUi': True,
            'strict': True
        }
    }
}
```

## 조건부 서식

행 배경색을 드롭다운 선택값에 따라 자동 변경한다:

| 조건 | 배경색 | 우선순위 |
|------|--------|---------|
| I열 또는 J열에 "Fail" | `#fef2f2` (빨간) | 1 (최우선) |
| I열 또는 J열에 "Pass" (Fail 없을 때만) | `#eff6ff` (파란) | 2 |

수식:
- Fail: `=OR($I7="Fail",$J7="Fail")`
- Pass: `=AND(OR($I7="Pass",$J7="Pass"),$I7<>"Fail",$J7<>"Fail")`

적용 범위: TC 데이터 행 전체 (A~K열)

## 워크플로우 연동

1. **TC 확정 시** (셀프 체크 통과 후):
   - 로컬에 TC HTML 생성
   - 사용자에게 Google Sheets 시트 추가 여부 질문
   - 추가할 시트 URL 질문
   - 시트 추가 시도 (권한 실패 시 Service Account 이메일 안내)
   - 시트 추가 후 Jira Epic Description에 스프레드시트 링크 추가
2. **TC 업데이트 시**:
   - 기존 시트의 데이터를 클리어 후 재작성
   - 통계 수식 범위도 함께 갱신
3. **이전 차수 참조**:
   - 같은 스프레드시트에 이전 차수 시트가 있으므로, TC 생성 시 기존 체크리스트를 읽어 누락 체크 가능

## 주의사항

- Service Account의 Drive 용량 제한으로 **새 파일 생성은 불가** — 기존 파일에 시트 추가만 가능
- `value_input_option='USER_ENTERED'`를 써야 수식이 동작함
- 조건부 서식은 `batch_update`의 `addConditionalFormatRule`로 설정
- Fail 규칙의 index를 0으로 설정하여 Pass보다 우선 적용

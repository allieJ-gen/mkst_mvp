


## 김엄마 신입생 상담 — Google Apps Script 구성 가이드

이 폴더는 웹앱(설문 입력)과 시트 바운드(관리자 팝업) Apps Script 코드를 보관합니다. 실제 서비스는 Apps Script 에디터에 붙여 넣어 배포하세요.

### 1) 준비물
- Google 스프레드시트 1개 생성(응답 저장용)
- 아래 값을 Apps Script 프로젝트의 스크립트 속성(PropertiesService)에 설정
  - `SPREADSHEET_ID`: 위 스프레드시트 ID
  - `ADMIN_EMAILS`: `mkst.system@gmail.com,mkst.functional@gmail.com` (쉼표로 추가 가능)

### 2) 웹앱(설문 입력)
1. Apps Script Standalone 프로젝트 생성 후, `webapp/Code.gs`, `webapp/index.html` 내용을 각각 파일에 붙여넣기
2. 프로젝트 설정 → 스크립트 속성에 `SPREADSHEET_ID`, `ADMIN_EMAILS` 설정
   - 선택(권장): `RESPONSES_SHEET_NAME`를 `ThisCohort`로 지정 가능(미지정 시 자동 탐색 규칙 사용)
3. 배포 → 새로운 배포 → 유형: 웹 앱
   - 실행자: 본인(Owner)
   - 액세스: 링크 보유자(또는 도메인 제한)
4. 배포 URL을 받으면 사용자 설문 페이지로 사용

### 3) 관리자 팝업(시트 바운드)
1. 응답 저장용 스프레드시트에서 확장 프로그램 → 앱스 스크립트 → 바운드 프로젝트 열기
2. `sheet-bound/Code.gs`, `sheet-bound/admin.html` 내용을 붙여넣기
3. 동일한 스크립트 속성(`SPREADSHEET_ID`, `ADMIN_EMAILS`) 설정
4. 스프레드시트로 돌아와 새로고침 → 상단 메뉴에 `관리자 뷰어` 생성됨
5. `관리자 뷰어 → 학생 검색 팝업 열기` 실행 후 이름으로 검색/코멘트 편집

### 4) 주요 정책 반영 사항
- 학년 `기타` 선택 시 자유 입력 필드는 제공하지 않습니다.
- 동일 이름/학교 중복 제출 허용(각 응답은 `respondentId`로 식별)
- 관리자 이메일 화이트리스트는 `ADMIN_EMAILS`(예: `mkst.system@gmail.com,mkst.functional@gmail.com`)에 저장하고 추후 추가 가능

### 5) 컬럼 스키마(`responses` 탭)
```
timestamp, respondentId, 이름, 학교, 학년, 계열, 탐구I, 탐구II,
주요과목등급, 전체평균,
국어_내신, 수학_내신, 영어_내신,
국어_모의, 수학_모의, 영어_모의,
탐구I_모의, 탐구II_모의,
기타과목명_모의, 기타_모의,
1지망_대학교, 2지망_대학교, 3지망_대학교,
1지망_학과, 2지망_학과, 3지망_학과,
이전공부법, 공부법변경이유, 김엄마선택이유, 김엄마에바라는점,
comment_admin, source, version
```

### 6) 배포 체크리스트
- 웹앱/시트 바운드 각각 스크립트 속성 설정 완료 확인
- 응답 시트 선택 규칙: `RESPONSES_SHEET_NAME` → `responses` → `ThisCohort` 순으로 사용
- 최초 실행 시 대상 시트가 없으면 `responses`를 자동 생성하고 헤더 삽입
- 웹앱 배포 후 URL 테스트: 제출 성공/실패 메시지 확인
- 관리자 팝업에서 이름 검색/코멘트 저장 검증

### 7) 배포/업데이트 운영 팁
- 코드가 변경되면(예: `index.html`, `Code.gs`) 웹앱 배포를 "다시 업데이트"해야 반영됩니다.
  - IDE: Deploy → Manage deployments → 웹앱 항목 연필 아이콘 → New version → Deploy(같은 URL 유지)
  - Test: Deploy → Test deployments → Web app(재배포 없이 최신 코드 테스트)
- 라이브러리로 배포하지 않기: New deployment에서 "Select type: Web app"을 꼭 선택하세요.
- 스크립트 속성/시트 데이터 변경은 재배포 없이 즉시 반영됩니다.

### 8) 관리자 이메일/권한 관리
- `ADMIN_EMAILS` 속성에 쉼표로 이메일을 추가하면 즉시 적용됩니다.
- 스프레드시트 공유(우상단 "공유")에서 해당 이메일에 보기 이상 권한을 부여해야 관리자 뷰어 사용 가능.

### 9) 변경 이력(최근)
- 폼 라벨의 "(필수)", "(0~100)" 안내 문구 제거(유효성은 그대로 유지)
- 관리자 뷰어에 서술형 4개 필드(이전공부법/공부법변경이유/김엄마선택이유/김엄마에바라는점) 표시 추가
- 시트명 자동 인식: `RESPONSES_SHEET_NAME` → `responses` → `ThisCohort`
- 운영 분리: 코드는 push로 올리고, 배포(Web app)는 사용자가 IDE에서 수행

### 10) CLI(선택) — push만 수행할 때
```bash
cd webapp && clasp push --force
# 배포는 IDE에서 Web app으로 직접 수행

cd ../sheet-bound && clasp push --force
# 시트 바운드 코드는 push만 하면 즉시 반영(배포 불필요)
```


# 김엄마관리형독서실 학생회원관리 시스템 MVP

독서실 운영을 위한 종합 학생 회원 관리 시스템입니다.

## 🏗️ 기술 스택

### Backend
- **Python 3.11**
- **Django 5.0** + Django REST Framework
- **PostgreSQL 15** (메인 데이터베이스)
- **Redis** (캐싱 & 세션)
- **JWT Authentication**

### Frontend
- **Node.js 22**
- **Vue.js** + **Nuxt.js 4**
- **@nuxt/ui** (UI 컴포넌트)

## 📋 주요 기능

### ✅ 완성된 기능 (Phase 3 완료)
- [x] 학생 CRUD API (생성/조회/수정/삭제)
- [x] 등원번호 자동 생성 (중복 방지)
- [x] 사물함 자동 배정/해제 시스템
- [x] 학생 검색 및 필터링
- [x] 통계 API (재원생/퇴원생/학년별/성별)
- [x] JWT 인증 시스템
- [x] Django Admin 완전 구성
- [x] API 문서화 (Swagger UI + ReDoc)

### 🔄 진행 예정
- [ ] Vue.js 프론트엔드 개발
- [ ] 실시간 알림 (Django Channels)
- [ ] 출석 관리 시스템
- [ ] 대시보드 UI

## 🚀 빠른 시작 가이드

### 1. 저장소 클론
```bash
git clone https://github.com/allieJ-gen/mkst_mvp.git
cd mkst_mvp
```

### 2. macOS 환경 설정 (자동 설치)
```bash
# 모든 필수 도구 자동 설치
bash setup_macos.sh
```

### 3. Python 환경 설정
```bash
python3.11 -m venv mkst_env
source mkst_env/bin/activate
pip install -r requirements.txt
```

### 4. 환경 변수 설정
```bash
cp config.env .env
# .env 파일을 편집하여 데이터베이스 정보 입력
```

### 5. 데이터베이스 설정
```bash
# PostgreSQL 데이터베이스 생성
createdb mkst_management

# Django 마이그레이션
python manage.py migrate

# 관리자 계정 생성
python manage.py createsuperuser

# 초기 데이터 설정 (271개 사물함)
python manage.py setup_initial_data

# 샘플 학생 데이터 생성 (8명)
python manage.py create_sample_data --count 8
```

### 6. 서버 실행
```bash
python manage.py runserver
```

## 🔗 주요 URL

- **Django Admin**: http://127.0.0.1:8000/admin/
- **API 문서 (Swagger)**: http://127.0.0.1:8000/api/docs/
- **API 문서 (ReDoc)**: http://127.0.0.1:8000/api/redoc/
- **학생 API**: http://127.0.0.1:8000/api/students/

## 📊 API 엔드포인트

### 인증
- `POST /api/auth/token/` - JWT 토큰 획득
- `POST /api/auth/token/refresh/` - 토큰 갱신

### 학생 관리
- `GET /api/students/` - 학생 목록 조회
- `POST /api/students/` - 새 학생 등록
- `GET /api/students/{id}/` - 특정 학생 조회
- `PUT /api/students/{id}/` - 학생 정보 수정
- `DELETE /api/students/{id}/` - 학생 삭제

### 특별 기능
- `POST /api/students/generate-attendance-number/` - 등원번호 생성
- `GET /api/students/active-students/` - 재원생만 조회
- `GET /api/students/statistics/` - 통계 정보
- `POST /api/students/{id}/assign-locker/` - 사물함 배정
- `POST /api/students/{id}/release-locker/` - 사물함 해제

## 📁 프로젝트 구조

```
mkst_mvp/
├── apps/
│   ├── students/       # 학생 관리 앱
│   ├── lockers/        # 사물함 관리 앱
│   ├── accounts/       # 사용자 계정 앱
│   └── dashboard/      # 대시보드 앱
├── mkst_management/    # Django 설정
├── frontend/           # Vue.js 프론트엔드
├── requirements.txt    # Python 의존성
├── setup_macos.sh     # macOS 설치 스크립트
└── README.md          # 이 파일
```

## 🗄️ 데이터베이스 모델

### Student (학생)
- 고유 ID, 등원번호, 이름, 학교, 학년
- 성별, 사물함번호, 첫등원일, 상태
- 학생/보호자 연락처

### Locker (사물함)
- 271개 사물함 (1~271번)
- 배정 상태, 배정된 학생 정보
- 배정/해제 이력 관리

## 💾 개발 기록

- **2025년 8월 11일**: Phase 3 백엔드 API 개발 완료
- 전체 진행률: ~60% 완료
- 다음 단계: Vue.js 프론트엔드 개발

## 📞 지원

문제가 발생하면 GitHub Issues를 통해 문의해주세요.

---

**개발자**: 김엄마관리형독서실  
**라이선스**: Private (내부 사용 전용)

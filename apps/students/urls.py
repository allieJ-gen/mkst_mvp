from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import StudentViewSet

# DRF Router를 사용하여 ViewSet을 URL에 자동 매핑
router = DefaultRouter()
router.register(r'students', StudentViewSet, basename='student')

app_name = 'students'

urlpatterns = [
    # API 엔드포인트들
    path('', include(router.urls)),
]

# 생성되는 URL 패턴들:
# GET    /api/students/                     - 학생 목록 조회
# POST   /api/students/                     - 학생 생성
# GET    /api/students/{id}/                - 학생 상세 조회
# PUT    /api/students/{id}/                - 학생 정보 수정
# PATCH  /api/students/{id}/                - 학생 정보 부분 수정
# DELETE /api/students/{id}/                - 학생 삭제
# POST   /api/students/generate-attendance-number/ - 등원번호 생성
# GET    /api/students/active-students/     - 재원생만 조회
# GET    /api/students/statistics/          - 학생 통계
# POST   /api/students/{id}/assign-locker/  - 사물함 배정
# POST   /api/students/{id}/release-locker/ - 사물함 해제


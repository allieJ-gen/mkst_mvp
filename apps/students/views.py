from rest_framework import viewsets, status, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Q
from django.contrib.auth.models import User

from .models import Student
from .serializers import (
    StudentSerializer,
    StudentCreateSerializer, 
    StudentListSerializer,
    AttendanceNumberGenerateSerializer
)

class StudentViewSet(viewsets.ModelViewSet):
    """학생 관리 API ViewSet - CRUD 및 검색 기능 제공"""
    
    queryset = Student.objects.all().order_by('-created_at')
    # permission_classes = [IsAuthenticated]  # 임시로 주석 처리 (테스트용)
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    
    # 필터링 가능한 필드들
    filterset_fields = {
        'status': ['exact'],
        'grade': ['exact'], 
        'gender': ['exact'],
        'school': ['icontains'],  # 부분 일치 검색
        'locker_number': ['exact', 'isnull'],  # 사물함 번호 또는 미배정
    }
    
    # 검색 가능한 필드들 (부분 일치)
    search_fields = ['attendance_number', 'name', 'school', 'parent_phone']
    
    # 정렬 가능한 필드들
    ordering_fields = ['created_at', 'name', 'grade', 'first_attendance_date']
    ordering = ['-created_at']  # 기본 정렬: 최신 등록순
    
    def get_serializer_class(self):
        """액션에 따라 다른 Serializer 사용"""
        if self.action == 'list':
            return StudentListSerializer  # 목록 조회시 간단한 정보만
        elif self.action == 'create':
            return StudentCreateSerializer  # 생성시 필요한 필드만
        return StudentSerializer  # 나머지는 전체 정보
    
    def get_queryset(self):
        """쿠리셋 커스터마이징 - 재원생 우선 표시"""
        queryset = Student.objects.all()
        
        # 재원생 우선 정렬 (재원생 먼저, 그 다음 최신 등록순)
        queryset = queryset.order_by(
            '-status',  # active가 먼저 오도록
            '-created_at'
        )
        
        return queryset
    
    def perform_create(self, serializer):
        """학생 생성 시 생성자 정보 자동 설정"""
        # 인증된 사용자가 있는 경우에만 설정
        if self.request.user.is_authenticated:
            serializer.save(
                created_by=self.request.user,
                updated_by=self.request.user
            )
        else:
            # 인증되지 않은 사용자의 경우 None으로 설정
            serializer.save(
                created_by=None,
                updated_by=None
            )
    
    def perform_update(self, serializer):
        """학생 수정 시 수정자 정보 자동 업데이트"""
        serializer.save(updated_by=self.request.user)
    
    @action(detail=False, methods=['post'], url_path='generate-attendance-number')
    def generate_attendance_number(self, request):
        """등원번호 생성 API - 보호자 휴대폰번호로 중복되지 않는 등원번호 생성"""
        serializer = AttendanceNumberGenerateSerializer(data=request.data)
        
        if serializer.is_valid():
            parent_phone = serializer.validated_data['parent_phone']
            
            try:
                # Student 모델의 generate_attendance_number 메서드 사용
                attendance_number = Student.generate_attendance_number(parent_phone)
                
                return Response({
                    'success': True,
                    'attendance_number': attendance_number,
                    'parent_phone': parent_phone,
                    'message': f'등원번호 {attendance_number}가 생성되었습니다.'
                }, status=status.HTTP_200_OK)
                
            except Exception as e:
                return Response({
                    'success': False,
                    'error': str(e),
                    'message': '등원번호 생성 중 오류가 발생했습니다.'
                }, status=status.HTTP_400_BAD_REQUEST)
        
        return Response({
            'success': False,
            'errors': serializer.errors,
            'message': '입력 데이터를 확인해주세요.'
        }, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=False, methods=['get'], url_path='active-students')
    def active_students(self, request):
        """재원생만 조회 API"""
        active_students = self.get_queryset().filter(status='active')
        
        # 페이지네이션 적용
        page = self.paginate_queryset(active_students)
        if page is not None:
            serializer = StudentListSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        
        serializer = StudentListSerializer(active_students, many=True)
        return Response({
            'count': active_students.count(),
            'results': serializer.data
        })
    
    @action(detail=False, methods=['get'], url_path='statistics')
    def statistics(self, request):
        """학생 통계 정보 API"""
        total_students = Student.objects.count()
        active_students = Student.objects.filter(status='active').count()
        withdrawn_students = Student.objects.filter(status='withdrawn').count()
        graduated_students = Student.objects.filter(status='graduated').count()
        expelled_students = Student.objects.filter(status='expelled').count()
        
        # 학년별 통계
        grade_stats = {}
        for grade in [1, 2, 3]:
            grade_stats[f'grade_{grade}'] = Student.objects.filter(
                grade=grade, status='active'
            ).count()
        
        # 성별 통계
        gender_stats = {
            'male': Student.objects.filter(gender='M', status='active').count(),
            'female': Student.objects.filter(gender='F', status='active').count()
        }
        
        # 사물함 통계
        locker_stats = {
            'assigned': Student.objects.filter(locker_number__isnull=False).count(),
            'unassigned': Student.objects.filter(locker_number__isnull=True).count()
        }
        
        return Response({
            'total_students': total_students,
            'status_breakdown': {
                'active': active_students,
                'withdrawn': withdrawn_students,
                'graduated': graduated_students,
                'expelled': expelled_students
            },
            'grade_breakdown': grade_stats,
            'gender_breakdown': gender_stats,
            'locker_breakdown': locker_stats
        })
    
    @action(detail=True, methods=['post'], url_path='assign-locker')
    def assign_locker(self, request, pk=None):
        """학생에게 사물함 배정 API"""
        student = self.get_object()
        
        try:
            locker_number = student.assign_locker()
            return Response({
                'success': True,
                'locker_number': locker_number,
                'message': f'{student.name} 학생에게 {locker_number}번 사물함이 배정되었습니다.'
            })
        except Exception as e:
            return Response({
                'success': False,
                'error': str(e),
                'message': '사물함 배정 중 오류가 발생했습니다.'
            }, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=True, methods=['post'], url_path='release-locker')
    def release_locker(self, request, pk=None):
        """학생의 사물함 해제 API"""
        student = self.get_object()
        
        try:
            released_locker = student.release_locker()
            return Response({
                'success': True,
                'released_locker': released_locker,
                'message': f'{student.name} 학생의 {released_locker}번 사물함이 해제되었습니다.'
            })
        except Exception as e:
            return Response({
                'success': False,
                'error': str(e),
                'message': '사물함 해제 중 오류가 발생했습니다.'
            }, status=status.HTTP_400_BAD_REQUEST)

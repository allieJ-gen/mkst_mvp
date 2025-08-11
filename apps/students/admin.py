from django.contrib import admin
from .models import Student


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    """학생 관리 Admin 인터페이스"""
    
    # 목록 화면 설정
    list_display = [
        'attendance_number', 'name', 'school', 'grade_display', 
        'gender', 'status_display', 'locker_number', 'first_attendance_date'
    ]
    
    list_filter = [
        'status', 'grade', 'gender', 'school', 'first_attendance_date'
    ]
    
    search_fields = [
        'attendance_number', 'name', 'school', 
        'student_phone', 'parent_phone'
    ]
    
    # 목록에서 재원생을 우선 표시
    ordering = ['status', '-created_at']
    
    # 상세 화면 설정
    fieldsets = (
        ('기본 정보', {
            'fields': ('attendance_number', 'name', 'school', 'grade', 'gender')
        }),
        ('사물함 정보', {
            'fields': ('locker_number',),
            'description': '사물함은 자동으로 배정됩니다.'
        }),
        ('등원/퇴원 정보', {
            'fields': ('first_attendance_date', 'status', 'withdrawal_date')
        }),
        ('연락처 정보', {
            'fields': ('student_phone', 'parent_phone')
        }),
        ('메타데이터', {
            'fields': ('created_by', 'updated_by'),
            'classes': ('collapse',)
        })
    )
    
    readonly_fields = ['created_at', 'updated_at']
    
    # 페이지당 표시 개수
    list_per_page = 50
    
    # 액션 추가
    actions = ['make_active', 'make_withdrawn']
    
    def make_active(self, request, queryset):
        """선택된 학생들을 재원생으로 변경"""
        updated = queryset.update(status='ACTIVE')
        self.message_user(request, f'{updated}명의 학생을 재원생으로 변경했습니다.')
    make_active.short_description = "선택된 학생을 재원생으로 변경"
    
    def make_withdrawn(self, request, queryset):
        """선택된 학생들을 퇴원생으로 변경"""
        updated = queryset.update(status='WITHDRAWN')
        self.message_user(request, f'{updated}명의 학생을 퇴원생으로 변경했습니다.')
    make_withdrawn.short_description = "선택된 학생을 퇴원생으로 변경"
    
    def save_model(self, request, obj, form, change):
        """모델 저장시 생성자/수정자 정보 자동 설정"""
        if not change:  # 새로 생성하는 경우
            obj.created_by = request.user
        obj.updated_by = request.user
        super().save_model(request, obj, form, change)
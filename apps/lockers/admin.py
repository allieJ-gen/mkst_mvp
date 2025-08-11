from django.contrib import admin
from .models import Locker, LockerHistory


@admin.register(Locker)
class LockerAdmin(admin.ModelAdmin):
    """사물함 관리 Admin 인터페이스"""
    
    # 목록 화면 설정
    list_display = [
        'number', 'is_occupied', 'student_name', 'assigned_date', 'usage_duration'
    ]
    
    list_filter = [
        'is_occupied', 'assigned_date', 'released_date'
    ]
    
    search_fields = [
        'number', 'student__name', 'student__attendance_number'
    ]
    
    ordering = ['number']
    
    # 상세 화면 설정
    fieldsets = (
        ('사물함 정보', {
            'fields': ('number', 'is_occupied')
        }),
        ('사용자 정보', {
            'fields': ('student',)
        }),
        ('사용 기간', {
            'fields': ('assigned_date', 'released_date')
        }),
        ('메타데이터', {
            'fields': ('created_at', 'updated_at', 'updated_by'),
            'classes': ('collapse',)
        })
    )
    
    readonly_fields = ['created_at', 'updated_at', 'usage_duration']
    
    # 페이지당 표시 개수
    list_per_page = 50
    
    # 액션 추가
    actions = ['release_selected_lockers']
    
    def student_name(self, obj):
        """학생 이름 표시"""
        return obj.student.name if obj.student else '-'
    student_name.short_description = '사용 학생'
    
    def release_selected_lockers(self, request, queryset):
        """선택된 사물함들을 해제"""
        released_count = 0
        for locker in queryset.filter(is_occupied=True):
            locker.release()
            released_count += 1
        self.message_user(request, f'{released_count}개의 사물함을 해제했습니다.')
    release_selected_lockers.short_description = "선택된 사물함 해제"
    
    def save_model(self, request, obj, form, change):
        """모델 저장시 수정자 정보 자동 설정"""
        obj.updated_by = request.user
        super().save_model(request, obj, form, change)


@admin.register(LockerHistory)
class LockerHistoryAdmin(admin.ModelAdmin):
    """사물함 이력 Admin 인터페이스"""
    
    # 목록 화면 설정
    list_display = [
        'locker_number', 'student_name', 'action', 'action_date', 'performed_by'
    ]
    
    list_filter = [
        'action', 'action_date', 'performed_by'
    ]
    
    search_fields = [
        'locker__number', 'student__name', 'student__attendance_number', 'notes'
    ]
    
    ordering = ['-action_date']
    
    # 상세 화면 설정
    fieldsets = (
        ('기본 정보', {
            'fields': ('locker', 'student', 'action')
        }),
        ('실행 정보', {
            'fields': ('action_date', 'performed_by')
        }),
        ('비고', {
            'fields': ('notes',)
        })
    )
    
    readonly_fields = ['action_date']
    
    # 페이지당 표시 개수
    list_per_page = 100
    
    def locker_number(self, obj):
        """사물함 번호 표시"""
        return f"{obj.locker.number}번"
    locker_number.short_description = '사물함'
    
    def student_name(self, obj):
        """학생 이름 표시"""
        return obj.student.name
    student_name.short_description = '학생'
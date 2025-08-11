from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from .models import UserProfile, ActivityLog


# 기존 User Admin을 확장하여 UserProfile 인라인 추가
class UserProfileInline(admin.StackedInline):
    """사용자 프로필 인라인"""
    model = UserProfile
    can_delete = False
    verbose_name_plural = '프로필'
    
    fieldsets = (
        ('역할 및 권한', {
            'fields': ('role', 'department')
        }),
        ('개인 정보', {
            'fields': ('phone_number', 'hire_date')
        }),
        ('상태', {
            'fields': ('is_active_staff',)
        })
    )


# User Admin 재정의
class UserAdmin(BaseUserAdmin):
    """확장된 사용자 Admin"""
    inlines = (UserProfileInline,)
    
    # 목록 화면에 역할 정보 추가
    list_display = BaseUserAdmin.list_display + ('get_role', 'get_department')
    list_filter = BaseUserAdmin.list_filter + ('profile__role', 'profile__is_active_staff')
    
    def get_role(self, obj):
        """사용자 역할 표시"""
        if hasattr(obj, 'profile'):
            return obj.profile.get_role_display()
        return '-'
    get_role.short_description = '역할'
    
    def get_department(self, obj):
        """부서 정보 표시"""
        if hasattr(obj, 'profile'):
            return obj.profile.department or '-'
        return '-'
    get_department.short_description = '부서'


# 기존 User Admin 등록 해제 후 새로운 Admin 등록
admin.site.unregister(User)
admin.site.register(User, UserAdmin)


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    """사용자 프로필 Admin 인터페이스"""
    
    # 목록 화면 설정
    list_display = [
        'user_full_name', 'role', 'department', 'phone_number', 
        'is_active_staff', 'hire_date'
    ]
    
    list_filter = [
        'role', 'department', 'is_active_staff', 'hire_date'
    ]
    
    search_fields = [
        'user__username', 'user__first_name', 'user__last_name',
        'user__email', 'phone_number', 'department'
    ]
    
    ordering = ['role', 'user__username']
    
    # 상세 화면 설정
    fieldsets = (
        ('사용자 정보', {
            'fields': ('user',)
        }),
        ('역할 및 권한', {
            'fields': ('role', 'department')
        }),
        ('개인 정보', {
            'fields': ('phone_number', 'hire_date')
        }),
        ('상태', {
            'fields': ('is_active_staff',)
        }),
        ('메타데이터', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        })
    )
    
    readonly_fields = ['created_at', 'updated_at']
    
    # 페이지당 표시 개수
    list_per_page = 25
    
    def user_full_name(self, obj):
        """사용자 전체 이름 표시"""
        return obj.full_name
    user_full_name.short_description = '이름'


@admin.register(ActivityLog)
class ActivityLogAdmin(admin.ModelAdmin):
    """활동 로그 Admin 인터페이스"""
    
    # 목록 화면 설정
    list_display = [
        'user', 'action', 'target_model', 'target_id', 
        'description_short', 'timestamp'
    ]
    
    list_filter = [
        'action', 'target_model', 'timestamp', 'user'
    ]
    
    search_fields = [
        'user__username', 'description', 'target_model', 'ip_address'
    ]
    
    ordering = ['-timestamp']
    
    # 상세 화면 설정
    fieldsets = (
        ('기본 정보', {
            'fields': ('user', 'action', 'description')
        }),
        ('대상 정보', {
            'fields': ('target_model', 'target_id')
        }),
        ('접속 정보', {
            'fields': ('ip_address', 'user_agent', 'timestamp')
        })
    )
    
    readonly_fields = ['timestamp']
    
    # 페이지당 표시 개수
    list_per_page = 100
    
    def description_short(self, obj):
        """설명 요약 표시"""
        return obj.description[:50] + '...' if len(obj.description) > 50 else obj.description
    description_short.short_description = '설명'
    
    # 읽기 전용으로 설정 (로그는 수정 불가)
    def has_change_permission(self, request, obj=None):
        return False
    
    def has_add_permission(self, request):
        return False
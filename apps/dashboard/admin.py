from django.contrib import admin
from .models import DashboardStats, SystemSettings, Announcement


@admin.register(DashboardStats)
class DashboardStatsAdmin(admin.ModelAdmin):
    """대시보드 통계 Admin 인터페이스"""
    
    # 목록 화면 설정
    list_display = [
        'stat_type', 'stat_date', 'active_students', 'total_students',
        'occupied_lockers', 'locker_usage_rate', 'created_at'
    ]
    
    list_filter = [
        'stat_type', 'stat_date', 'created_at'
    ]
    
    search_fields = [
        'stat_date',
    ]
    
    ordering = ['-stat_date', 'stat_type']
    
    # 상세 화면 설정
    fieldsets = (
        ('기본 정보', {
            'fields': ('stat_type', 'stat_date')
        }),
        ('학생 통계', {
            'fields': (
                'total_students', 'active_students', 
                'new_students', 'withdrawn_students'
            )
        }),
        ('학년별 분포', {
            'fields': (
                'grade_0_count', 'grade_1_count', 
                'grade_2_count', 'grade_3_count'
            )
        }),
        ('성별 분포', {
            'fields': ('male_count', 'female_count')
        }),
        ('사물함 통계', {
            'fields': (
                'total_lockers', 'occupied_lockers', 
                'available_lockers', 'locker_usage_rate'
            )
        }),
        ('메타데이터', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        })
    )
    
    readonly_fields = ['created_at', 'updated_at']
    
    # 페이지당 표시 개수
    list_per_page = 50
    
    # 액션 추가
    actions = ['generate_daily_stats']
    
    def generate_daily_stats(self, request, queryset):
        """선택된 날짜의 일별 통계 재생성"""
        from django.utils import timezone
        
        generated_count = 0
        for stats in queryset:
            DashboardStats.generate_daily_stats(stats.stat_date)
            generated_count += 1
            
        self.message_user(request, f'{generated_count}개의 통계를 재생성했습니다.')
    generate_daily_stats.short_description = "선택된 날짜의 통계 재생성"


@admin.register(SystemSettings)
class SystemSettingsAdmin(admin.ModelAdmin):
    """시스템 설정 Admin 인터페이스"""
    
    # 목록 화면 설정
    list_display = [
        'key', 'value_short', 'setting_type', 'is_active', 
        'updated_at', 'updated_by'
    ]
    
    list_filter = [
        'setting_type', 'is_active', 'updated_at'
    ]
    
    search_fields = [
        'key', 'value', 'description'
    ]
    
    ordering = ['setting_type', 'key']
    
    # 상세 화면 설정
    fieldsets = (
        ('기본 정보', {
            'fields': ('key', 'value', 'setting_type')
        }),
        ('설명', {
            'fields': ('description',)
        }),
        ('상태', {
            'fields': ('is_active',)
        }),
        ('메타데이터', {
            'fields': ('created_at', 'updated_at', 'updated_by'),
            'classes': ('collapse',)
        })
    )
    
    readonly_fields = ['created_at', 'updated_at']
    
    # 페이지당 표시 개수
    list_per_page = 50
    
    def value_short(self, obj):
        """설정값 요약 표시"""
        return obj.value[:30] + '...' if len(obj.value) > 30 else obj.value
    value_short.short_description = '설정값'
    
    def save_model(self, request, obj, form, change):
        """모델 저장시 수정자 정보 자동 설정"""
        obj.updated_by = request.user
        super().save_model(request, obj, form, change)


@admin.register(Announcement)
class AnnouncementAdmin(admin.ModelAdmin):
    """공지사항 Admin 인터페이스"""
    
    # 목록 화면 설정
    list_display = [
        'title', 'priority', 'is_active', 'is_pinned', 
        'start_date', 'end_date', 'created_by'
    ]
    
    list_filter = [
        'priority', 'is_active', 'is_pinned', 'start_date', 'created_by'
    ]
    
    search_fields = [
        'title', 'content'
    ]
    
    ordering = ['-is_pinned', '-priority', '-created_at']
    
    # 상세 화면 설정
    fieldsets = (
        ('기본 정보', {
            'fields': ('title', 'content')
        }),
        ('설정', {
            'fields': ('priority', 'is_active', 'is_pinned')
        }),
        ('표시 기간', {
            'fields': ('start_date', 'end_date'),
            'description': '종료일을 비워두면 계속 표시됩니다.'
        }),
        ('메타데이터', {
            'fields': ('created_by', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        })
    )
    
    readonly_fields = ['created_at', 'updated_at']
    
    # 페이지당 표시 개수
    list_per_page = 25
    
    # 액션 추가
    actions = ['make_active', 'make_inactive', 'pin_announcements']
    
    def make_active(self, request, queryset):
        """선택된 공지사항을 활성화"""
        updated = queryset.update(is_active=True)
        self.message_user(request, f'{updated}개의 공지사항을 활성화했습니다.')
    make_active.short_description = "선택된 공지사항 활성화"
    
    def make_inactive(self, request, queryset):
        """선택된 공지사항을 비활성화"""
        updated = queryset.update(is_active=False)
        self.message_user(request, f'{updated}개의 공지사항을 비활성화했습니다.')
    make_inactive.short_description = "선택된 공지사항 비활성화"
    
    def pin_announcements(self, request, queryset):
        """선택된 공지사항을 상단 고정"""
        updated = queryset.update(is_pinned=True)
        self.message_user(request, f'{updated}개의 공지사항을 상단에 고정했습니다.')
    pin_announcements.short_description = "선택된 공지사항 상단 고정"
    
    def save_model(self, request, obj, form, change):
        """모델 저장시 작성자 정보 자동 설정"""
        if not change:  # 새로 생성하는 경우
            obj.created_by = request.user
        super().save_model(request, obj, form, change)
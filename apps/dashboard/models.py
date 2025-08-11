from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.db.models import Count, Q
from datetime import datetime, timedelta


class DashboardStats(models.Model):
    """
    대시보드 통계 캐시 모델
    복잡한 통계 계산 결과를 캐시하여 성능 향상
    """
    
    STAT_TYPE_CHOICES = [
        ('DAILY', '일별 통계'),
        ('WEEKLY', '주별 통계'),
        ('MONTHLY', '월별 통계'),
        ('YEARLY', '연별 통계'),
    ]
    
    stat_type = models.CharField(
        max_length=10,
        choices=STAT_TYPE_CHOICES,
        verbose_name="통계 유형"
    )
    
    stat_date = models.DateField(
        verbose_name="통계 날짜"
    )
    
    # 학생 관련 통계
    total_students = models.IntegerField(
        default=0,
        verbose_name="전체 학생 수"
    )
    
    active_students = models.IntegerField(
        default=0,
        verbose_name="재원생 수"
    )
    
    new_students = models.IntegerField(
        default=0,
        verbose_name="신규 등록 학생 수"
    )
    
    withdrawn_students = models.IntegerField(
        default=0,
        verbose_name="퇴원 학생 수"
    )
    
    # 학년별 분포
    grade_0_count = models.IntegerField(default=0, verbose_name="비고등학생 수")
    grade_1_count = models.IntegerField(default=0, verbose_name="1학년 수")
    grade_2_count = models.IntegerField(default=0, verbose_name="2학년 수")
    grade_3_count = models.IntegerField(default=0, verbose_name="3학년 수")
    
    # 성별 분포
    male_count = models.IntegerField(default=0, verbose_name="남학생 수")
    female_count = models.IntegerField(default=0, verbose_name="여학생 수")
    
    # 사물함 관련 통계
    total_lockers = models.IntegerField(default=271, verbose_name="전체 사물함 수")
    occupied_lockers = models.IntegerField(default=0, verbose_name="사용중 사물함 수")
    available_lockers = models.IntegerField(default=271, verbose_name="사용 가능 사물함 수")
    locker_usage_rate = models.FloatField(default=0.0, verbose_name="사물함 이용률 (%)")
    
    # 메타데이터
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="생성일시")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="수정일시")
    
    class Meta:
        verbose_name = "대시보드 통계"
        verbose_name_plural = "대시보드 통계들"
        unique_together = ['stat_type', 'stat_date']
        ordering = ['-stat_date', 'stat_type']
        indexes = [
            models.Index(fields=['stat_type', 'stat_date']),
            models.Index(fields=['stat_date']),
        ]
    
    def __str__(self):
        stat_type_display = dict(self.STAT_TYPE_CHOICES)[self.stat_type]
        return f"{stat_type_display} - {self.stat_date}"
    
    @classmethod
    def generate_daily_stats(cls, target_date=None):
        """일별 통계 생성"""
        if target_date is None:
            target_date = timezone.now().date()
        
        from apps.students.models import Student
        from apps.lockers.models import Locker
        
        # 기존 통계 삭제 후 재생성
        cls.objects.filter(stat_type='DAILY', stat_date=target_date).delete()
        
        # 학생 통계 계산
        students_qs = Student.objects.all()
        active_students_qs = students_qs.filter(status='ACTIVE')
        
        # 신규 등록 학생 (해당 날짜에 등록)
        new_students = students_qs.filter(
            first_attendance_date=target_date
        ).count()
        
        # 퇴원 학생 (해당 날짜에 퇴원)
        withdrawn_students = students_qs.filter(
            withdrawal_date=target_date
        ).count()
        
        # 학년별 분포 (활성 학생만)
        grade_counts = active_students_qs.values('grade').annotate(
            count=Count('id')
        )
        grade_distribution = {0: 0, 1: 0, 2: 0, 3: 0}
        for item in grade_counts:
            grade_distribution[item['grade']] = item['count']
        
        # 성별 분포 (활성 학생만)
        gender_counts = active_students_qs.values('gender').annotate(
            count=Count('id')
        )
        gender_distribution = {'M': 0, 'F': 0}
        for item in gender_counts:
            gender_distribution[item['gender']] = item['count']
        
        # 사물함 통계
        locker_stats = Locker.get_usage_stats()
        
        # 통계 객체 생성
        stats = cls.objects.create(
            stat_type='DAILY',
            stat_date=target_date,
            total_students=students_qs.count(),
            active_students=active_students_qs.count(),
            new_students=new_students,
            withdrawn_students=withdrawn_students,
            grade_0_count=grade_distribution[0],
            grade_1_count=grade_distribution[1],
            grade_2_count=grade_distribution[2],
            grade_3_count=grade_distribution[3],
            male_count=gender_distribution['M'],
            female_count=gender_distribution['F'],
            total_lockers=locker_stats['total'],
            occupied_lockers=locker_stats['occupied'],
            available_lockers=locker_stats['available'],
            locker_usage_rate=locker_stats['usage_rate']
        )
        
        return stats
    
    @classmethod
    def get_latest_stats(cls, stat_type='DAILY'):
        """최신 통계 조회"""
        return cls.objects.filter(stat_type=stat_type).first()
    
    @classmethod
    def get_trend_data(cls, stat_type='DAILY', days=7):
        """트렌드 데이터 조회 (최근 N일)"""
        end_date = timezone.now().date()
        start_date = end_date - timedelta(days=days-1)
        
        return cls.objects.filter(
            stat_type=stat_type,
            stat_date__range=[start_date, end_date]
        ).order_by('stat_date')


class SystemSettings(models.Model):
    """
    시스템 설정 모델
    다양한 시스템 설정값을 저장
    """
    
    SETTING_TYPE_CHOICES = [
        ('GENERAL', '일반 설정'),
        ('NOTIFICATION', '알림 설정'),
        ('BACKUP', '백업 설정'),
        ('DISPLAY', '표시 설정'),
    ]
    
    key = models.CharField(
        max_length=100,
        unique=True,
        verbose_name="설정 키"
    )
    
    value = models.TextField(
        verbose_name="설정 값"
    )
    
    setting_type = models.CharField(
        max_length=15,
        choices=SETTING_TYPE_CHOICES,
        default='GENERAL',
        verbose_name="설정 유형"
    )
    
    description = models.TextField(
        blank=True,
        verbose_name="설명"
    )
    
    is_active = models.BooleanField(
        default=True,
        verbose_name="활성화 여부"
    )
    
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="생성일시")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="수정일시")
    updated_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        verbose_name="수정자"
    )
    
    class Meta:
        verbose_name = "시스템 설정"
        verbose_name_plural = "시스템 설정들"
        ordering = ['setting_type', 'key']
    
    def __str__(self):
        return f"{self.key}: {self.value[:50]}..."
    
    @classmethod
    def get_setting(cls, key, default=None):
        """설정값 조회"""
        try:
            setting = cls.objects.get(key=key, is_active=True)
            return setting.value
        except cls.DoesNotExist:
            return default
    
    @classmethod
    def set_setting(cls, key, value, setting_type='GENERAL', description='', user=None):
        """설정값 저장"""
        setting, created = cls.objects.update_or_create(
            key=key,
            defaults={
                'value': value,
                'setting_type': setting_type,
                'description': description,
                'updated_by': user,
                'is_active': True
            }
        )
        return setting
    
    @classmethod
    def get_display_settings(cls):
        """표시 관련 설정들 조회"""
        return cls.objects.filter(
            setting_type='DISPLAY',
            is_active=True
        ).values('key', 'value')


class Announcement(models.Model):
    """
    공지사항 모델
    관리자용 공지사항 관리
    """
    
    PRIORITY_CHOICES = [
        ('LOW', '낮음'),
        ('NORMAL', '보통'),
        ('HIGH', '높음'),
        ('URGENT', '긴급'),
    ]
    
    title = models.CharField(
        max_length=200,
        verbose_name="제목"
    )
    
    content = models.TextField(
        verbose_name="내용"
    )
    
    priority = models.CharField(
        max_length=10,
        choices=PRIORITY_CHOICES,
        default='NORMAL',
        verbose_name="우선순위"
    )
    
    is_active = models.BooleanField(
        default=True,
        verbose_name="활성화 여부"
    )
    
    is_pinned = models.BooleanField(
        default=False,
        verbose_name="상단 고정"
    )
    
    # 표시 기간
    start_date = models.DateTimeField(
        default=timezone.now,
        verbose_name="표시 시작일"
    )
    
    end_date = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name="표시 종료일"
    )
    
    # 메타데이터
    created_by = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='created_announcements',
        verbose_name="작성자"
    )
    
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="작성일시")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="수정일시")
    
    class Meta:
        verbose_name = "공지사항"
        verbose_name_plural = "공지사항들"
        ordering = ['-is_pinned', '-priority', '-created_at']
        indexes = [
            models.Index(fields=['is_active', 'start_date', 'end_date']),
            models.Index(fields=['priority', 'created_at']),
        ]
    
    def __str__(self):
        priority_display = dict(self.PRIORITY_CHOICES)[self.priority]
        return f"[{priority_display}] {self.title}"
    
    @property
    def is_current(self):
        """현재 표시 중인 공지사항인지 확인"""
        now = timezone.now()
        if not self.is_active:
            return False
        if self.start_date > now:
            return False
        if self.end_date and self.end_date < now:
            return False
        return True
    
    @classmethod
    def get_active_announcements(cls):
        """현재 활성화된 공지사항 조회"""
        now = timezone.now()
        return cls.objects.filter(
            is_active=True,
            start_date__lte=now
        ).filter(
            Q(end_date__isnull=True) | Q(end_date__gte=now)
        ).order_by('-is_pinned', '-priority', '-created_at')

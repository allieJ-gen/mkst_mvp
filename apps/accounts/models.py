from django.db import models
from django.contrib.auth.models import AbstractUser, User
from django.utils import timezone


class UserProfile(models.Model):
    """
    사용자 프로필 확장 모델
    Django 기본 User 모델을 확장하여 관리자 정보 관리
    """
    
    ROLE_CHOICES = [
        ('ADMIN', '관리자'),
        ('STAFF', '직원'),
        ('MANAGER', '매니저'),
    ]
    
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='profile',
        verbose_name="사용자"
    )
    
    # 역할 및 권한
    role = models.CharField(
        max_length=10,
        choices=ROLE_CHOICES,
        default='STAFF',
        verbose_name="역할"
    )
    
    # 추가 정보
    phone_number = models.CharField(
        max_length=15,
        blank=True,
        verbose_name="연락처"
    )
    
    department = models.CharField(
        max_length=50,
        blank=True,
        verbose_name="부서"
    )
    
    # 근무 정보
    hire_date = models.DateField(
        null=True,
        blank=True,
        verbose_name="입사일"
    )
    
    is_active_staff = models.BooleanField(
        default=True,
        verbose_name="활성 직원 여부"
    )
    
    # 메타데이터
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="생성일시")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="수정일시")
    
    class Meta:
        verbose_name = "사용자 프로필"
        verbose_name_plural = "사용자 프로필들"
        ordering = ['-created_at']
    
    def __str__(self):
        role_display = dict(self.ROLE_CHOICES)[self.role]
        return f"{self.user.get_full_name() or self.user.username} ({role_display})"
    
    @property
    def full_name(self):
        """전체 이름"""
        return self.user.get_full_name() or self.user.username
    
    @property
    def is_admin(self):
        """관리자 여부"""
        return self.role == 'ADMIN'
    
    @property
    def is_manager(self):
        """매니저 여부"""
        return self.role in ['ADMIN', 'MANAGER']
    
    def can_manage_students(self):
        """학생 관리 권한 여부"""
        return self.role in ['ADMIN', 'MANAGER', 'STAFF']
    
    def can_manage_lockers(self):
        """사물함 관리 권한 여부"""
        return self.role in ['ADMIN', 'MANAGER', 'STAFF']
    
    def can_view_dashboard(self):
        """대시보드 조회 권한 여부"""
        return self.role in ['ADMIN', 'MANAGER', 'STAFF']


class ActivityLog(models.Model):
    """
    사용자 활동 로그 모델
    시스템 내 주요 활동을 추적
    """
    
    ACTION_CHOICES = [
        ('CREATE', '생성'),
        ('UPDATE', '수정'),
        ('DELETE', '삭제'),
        ('LOGIN', '로그인'),
        ('LOGOUT', '로그아웃'),
        ('VIEW', '조회'),
        ('EXPORT', '내보내기'),
    ]
    
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='activity_logs',
        verbose_name="사용자"
    )
    
    action = models.CharField(
        max_length=10,
        choices=ACTION_CHOICES,
        verbose_name="동작"
    )
    
    target_model = models.CharField(
        max_length=50,
        blank=True,
        verbose_name="대상 모델",
        help_text="Student, Locker 등"
    )
    
    target_id = models.PositiveIntegerField(
        null=True,
        blank=True,
        verbose_name="대상 ID"
    )
    
    description = models.TextField(
        verbose_name="설명"
    )
    
    ip_address = models.GenericIPAddressField(
        null=True,
        blank=True,
        verbose_name="IP 주소"
    )
    
    user_agent = models.TextField(
        blank=True,
        verbose_name="사용자 에이전트"
    )
    
    timestamp = models.DateTimeField(
        default=timezone.now,
        verbose_name="실행 시각"
    )
    
    class Meta:
        verbose_name = "활동 로그"
        verbose_name_plural = "활동 로그들"
        ordering = ['-timestamp']
        indexes = [
            models.Index(fields=['user', 'timestamp']),
            models.Index(fields=['action', 'timestamp']),
            models.Index(fields=['target_model', 'target_id']),
        ]
    
    def __str__(self):
        action_display = dict(self.ACTION_CHOICES)[self.action]
        return f"{self.user.username} - {action_display} ({self.timestamp.strftime('%Y-%m-%d %H:%M')})"
    
    @classmethod
    def log_activity(cls, user, action, description, target_model=None, target_id=None, 
                    ip_address=None, user_agent=None):
        """활동 로그 생성"""
        return cls.objects.create(
            user=user,
            action=action,
            target_model=target_model,
            target_id=target_id,
            description=description,
            ip_address=ip_address,
            user_agent=user_agent
        )


# Signal을 사용하여 User 생성시 자동으로 UserProfile 생성
from django.db.models.signals import post_save
from django.dispatch import receiver

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    """User 생성시 UserProfile 자동 생성"""
    if created:
        UserProfile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    """User 저장시 UserProfile도 저장"""
    if hasattr(instance, 'profile'):
        instance.profile.save()

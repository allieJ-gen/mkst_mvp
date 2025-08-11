from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.utils import timezone


class Locker(models.Model):
    """
    사물함 관리 모델
    1~271번 사물함과 휴대폰보관함을 통합 관리
    """
    
    # 사물함 번호 (Primary Key)
    number = models.IntegerField(
        primary_key=True,
        verbose_name="사물함번호",
        help_text="1~271번 사물함, 휴대폰보관함과 동일번호"
    )
    
    # 사용 상태
    is_occupied = models.BooleanField(
        default=False,
        verbose_name="사용중 여부"
    )
    
    # 사용 학생 정보 (외래키)
    student = models.OneToOneField(
        'students.Student',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='assigned_locker',
        verbose_name="사용 학생"
    )
    
    # 배정/해제 일시
    assigned_date = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name="배정일시"
    )
    released_date = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name="해제일시"
    )
    
    # 메타데이터
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="생성일시")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="수정일시")
    updated_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        related_name='updated_lockers',
        verbose_name="수정자"
    )
    
    class Meta:
        verbose_name = "사물함"
        verbose_name_plural = "사물함들"
        ordering = ['number']  # 번호순 정렬
        indexes = [
            models.Index(fields=['is_occupied']),
            models.Index(fields=['assigned_date']),
        ]
    
    def __str__(self):
        """사물함 번호와 사용 상태 표시"""
        status = "사용중" if self.is_occupied else "빈사물함"
        student_info = f" - {self.student.name}" if self.student else ""
        return f"{self.number}번 사물함 ({status}){student_info}"
    
    def clean(self):
        """모델 검증 로직"""
        super().clean()
        
        # 사물함 번호 범위 검증
        if not (1 <= self.number <= 271):
            raise ValidationError({
                'number': '사물함 번호는 1~271 범위여야 합니다.'
            })
        
        # 사용중 상태와 학생 정보 일치성 검증
        if self.is_occupied and not self.student:
            raise ValidationError({
                'student': '사용중인 사물함은 학생 정보가 필요합니다.'
            })
        
        if not self.is_occupied and self.student:
            raise ValidationError({
                'is_occupied': '학생이 배정된 사물함은 사용중 상태여야 합니다.'
            })
    
    def assign_to_student(self, student):
        """
        학생에게 사물함 배정
        """
        if self.is_occupied:
            raise ValidationError(f"{self.number}번 사물함은 이미 사용중입니다.")
        
        self.student = student
        self.is_occupied = True
        self.assigned_date = timezone.now()
        self.released_date = None
        self.save()
        
        # 학생 모델의 사물함 번호도 업데이트
        if student.locker_number != self.number:
            student.locker_number = self.number
            student.save(update_fields=['locker_number'])
    
    def release(self):
        """
        사물함 해제
        """
        if not self.is_occupied:
            raise ValidationError(f"{self.number}번 사물함은 이미 빈 상태입니다.")
        
        # 학생 모델의 사물함 번호 초기화
        if self.student:
            self.student.locker_number = None
            self.student.save(update_fields=['locker_number'])
        
        self.student = None
        self.is_occupied = False
        self.released_date = timezone.now()
        self.save()
    
    @classmethod
    def get_available_lockers(cls):
        """사용 가능한 사물함 목록 조회"""
        return cls.objects.filter(is_occupied=False).order_by('number')
    
    @classmethod
    def get_occupied_lockers(cls):
        """사용중인 사물함 목록 조회"""
        return cls.objects.filter(is_occupied=True).select_related('student').order_by('number')
    
    @classmethod
    def get_usage_stats(cls):
        """사물함 이용 통계"""
        total = cls.objects.count()
        occupied = cls.objects.filter(is_occupied=True).count()
        available = total - occupied
        usage_rate = (occupied / total * 100) if total > 0 else 0
        
        return {
            'total': total,
            'occupied': occupied,
            'available': available,
            'usage_rate': round(usage_rate, 1)
        }
    
    @property
    def usage_duration(self):
        """현재 사용 기간 (일수)"""
        if not self.is_occupied or not self.assigned_date:
            return 0
        return (timezone.now() - self.assigned_date).days


class LockerHistory(models.Model):
    """
    사물함 사용 이력 모델
    사물함 배정/해제 이력을 추적
    """
    
    ACTION_CHOICES = [
        ('ASSIGN', '배정'),
        ('RELEASE', '해제'),
        ('TRANSFER', '이동'),
    ]
    
    locker = models.ForeignKey(
        Locker,
        on_delete=models.CASCADE,
        related_name='history',
        verbose_name="사물함"
    )
    
    student = models.ForeignKey(
        'students.Student',
        on_delete=models.CASCADE,
        related_name='locker_history',
        verbose_name="학생"
    )
    
    action = models.CharField(
        max_length=10,
        choices=ACTION_CHOICES,
        verbose_name="동작"
    )
    
    # 이력 정보
    action_date = models.DateTimeField(
        default=timezone.now,
        verbose_name="동작일시"
    )
    
    performed_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        verbose_name="수행자"
    )
    
    notes = models.TextField(
        blank=True,
        verbose_name="비고"
    )
    
    class Meta:
        verbose_name = "사물함 이력"
        verbose_name_plural = "사물함 이력들"
        ordering = ['-action_date']
        indexes = [
            models.Index(fields=['locker', 'action_date']),
            models.Index(fields=['student', 'action_date']),
            models.Index(fields=['action']),
        ]
    
    def __str__(self):
        action_display = dict(self.ACTION_CHOICES)[self.action]
        return f"{self.locker.number}번 사물함 {action_display} - {self.student.name}"
    
    @classmethod
    def create_assign_history(cls, locker, student, user=None):
        """사물함 배정 이력 생성"""
        return cls.objects.create(
            locker=locker,
            student=student,
            action='ASSIGN',
            performed_by=user,
            notes=f"{student.name}에게 {locker.number}번 사물함 배정"
        )
    
    @classmethod
    def create_release_history(cls, locker, student, user=None):
        """사물함 해제 이력 생성"""
        return cls.objects.create(
            locker=locker,
            student=student,
            action='RELEASE',
            performed_by=user,
            notes=f"{student.name}의 {locker.number}번 사물함 해제"
        )

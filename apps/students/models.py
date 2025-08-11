from django.db import models
from django.contrib.auth.models import User
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError
from django.utils import timezone
import re
import random
import string


class Student(models.Model):
    """
    학생 정보 모델
    김엄마관리형독서실의 학생 회원 정보를 관리하는 핵심 모델
    """
    
    # 학년 선택지
    GRADE_CHOICES = [
        (0, '비고등학생'),
        (1, '1학년'),
        (2, '2학년'),
        (3, '3학년'),
    ]
    
    # 성별 선택지 (좌석 구분용)
    GENDER_CHOICES = [
        ('M', '남'),
        ('F', '여'),
    ]
    
    # 구분 상태 선택지
    STATUS_CHOICES = [
        ('active', '재원생'),
        ('withdrawn', '퇴원생'),
        ('graduated', '졸업생'),
        ('expelled', '강퇴생'),
    ]
    
    # 핵심 식별 정보
    id = models.AutoField(primary_key=True, verbose_name="학생 고유 ID")
    attendance_number = models.CharField(
        max_length=5, 
        unique=True, 
        verbose_name="등원번호",
        help_text="보호자 휴대폰 뒤4자리 + 핀번호 1자리"
    )
    
    # 기본 정보
    name = models.CharField(max_length=50, verbose_name="학생명")
    school = models.CharField(max_length=100, verbose_name="학교명", 
                             help_text="고등학교 접미어 생략 (예: 서현고등학교 → 서현)")
    grade = models.IntegerField(choices=GRADE_CHOICES, verbose_name="학년")
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, verbose_name="성별")
    
    # 사물함 정보
    locker_number = models.IntegerField(
        null=True, 
        blank=True, 
        verbose_name="사물함번호",
        help_text="1~271번 사물함, 휴대폰보관함과 동일번호"
    )
    
    # 등원/퇴원 정보
    first_attendance_date = models.DateField(verbose_name="첫등원일",
                                           help_text="재등록생의 경우 마지막 재등록일")
    status = models.CharField(
        max_length=10, 
        choices=STATUS_CHOICES, 
        default='ACTIVE',
        verbose_name="구분"
    )
    withdrawal_date = models.DateField(
        null=True, 
        blank=True, 
        verbose_name="퇴원일",
        help_text="마지막 등원일 + 1일"
    )
    
    # 연락처 정보
    student_phone = models.CharField(
        max_length=15, 
        null=True, 
        blank=True,
        verbose_name="학생 휴대폰번호",
        validators=[RegexValidator(
            regex=r'^010-\d{4}-\d{4}$',
            message='휴대폰번호는 010-0000-0000 형식으로 입력해주세요.'
        )]
    )
    parent_phone = models.CharField(
        max_length=15,
        verbose_name="보호자 휴대폰번호",
        validators=[RegexValidator(
            regex=r'^010-\d{4}-\d{4}$',
            message='휴대폰번호는 010-0000-0000 형식으로 입력해주세요.'
        )]
    )
    
    # 메타데이터
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="생성일시")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="수정일시")
    created_by = models.ForeignKey(
        User, 
        on_delete=models.SET_NULL, 
        null=True,
        related_name='created_students',
        verbose_name="생성자"
    )
    updated_by = models.ForeignKey(
        User, 
        on_delete=models.SET_NULL, 
        null=True,
        related_name='updated_students',
        verbose_name="수정자"
    )
    
    class Meta:
        verbose_name = "학생"
        verbose_name_plural = "학생들"
        ordering = ['-created_at']  # 최신 등록순
        indexes = [
            models.Index(fields=['attendance_number']),
            models.Index(fields=['name']),
            models.Index(fields=['school']),
            models.Index(fields=['status']),
            models.Index(fields=['locker_number']),
        ]
    
    def __str__(self):
        """학생명 + 등원번호로 표시"""
        return f"{self.name} ({self.attendance_number})"
    
    def clean(self):
        """모델 검증 로직"""
        super().clean()
        
        # 등원번호 형식 검증 (4~5자리 숫자)
        if self.attendance_number:
            if not re.match(r'^\d{4,5}$', self.attendance_number):
                raise ValidationError({
                    'attendance_number': '등원번호는 4~5자리 숫자여야 합니다.'
                })
        
        # 사물함 번호 범위 검증
        if self.locker_number is not None:
            if not (1 <= self.locker_number <= 271):
                raise ValidationError({
                    'locker_number': '사물함 번호는 1~271 범위여야 합니다.'
                })
        
        # 퇴원일 검증
        if self.withdrawal_date and self.first_attendance_date:
            if self.withdrawal_date <= self.first_attendance_date:
                raise ValidationError({
                    'withdrawal_date': '퇴원일은 첫등원일보다 이후여야 합니다.'
                })
    
    def save(self, *args, **kwargs):
        """저장 시 추가 로직"""
        # 등원번호가 없으면 자동 생성
        if not self.attendance_number and self.parent_phone:
            self.attendance_number = self.generate_attendance_number(self.parent_phone)
        
        # 사물함이 없으면 자동 배정
        if not self.locker_number and self.status == 'active':
            self.assign_locker()
        
        # 퇴원생으로 변경시 사물함 해제
        if self.status != 'active' and self.locker_number:
            try:
                self.release_locker()
            except Exception:
                pass  # 사물함 해제 실패시 무시
        
        super().save(*args, **kwargs)
    
    @classmethod
    def generate_attendance_number(cls, parent_phone):
        """
        보호자 휴대폰번호를 기반으로 등원번호 자동 생성
        형식: 보호자휴대폰 뒤4자리 + 핀번호 1자리
        """
        if not parent_phone:
            return None
        
        # 휴대폰번호에서 숫자만 추출
        phone_digits = re.sub(r'\D', '', parent_phone)
        if len(phone_digits) < 4:
            return None
        
        # 뒤 4자리 추출
        base_number = phone_digits[-4:]
        
        # 핀번호 1~9 순차적으로 시도
        for pin in range(1, 10):
            candidate = f"{base_number}{pin}"
            
            # 중복 체크
            if not cls.objects.filter(attendance_number=candidate).exists():
                return candidate
        
        # 1~9까지 모두 사용된 경우 랜덤 생성
        return cls.generate_random_attendance_number()
    
    @classmethod
    def generate_random_attendance_number(cls):
        """랜덤 등원번호 생성 (마지막 수단)"""
        for _ in range(100):  # 최대 100번 시도
            number = ''.join(random.choices(string.digits, k=5))
            if not cls.objects.filter(attendance_number=number).exists():
                return number
        return None
    
    def assign_locker(self):
        """사물함 자동 배정"""
        from apps.lockers.models import Locker
        
        # 이미 사물함이 있는 경우
        if self.locker_number:
            return self.locker_number
        
        # 사용 가능한 사물함 찾기
        available_locker = Locker.objects.filter(is_occupied=False).first()
        if available_locker:
            self.locker_number = available_locker.number
            available_locker.assign_to_student(self)
            self.save()
            return self.locker_number
        
        raise Exception("사용 가능한 사물함이 없습니다.")
    
    def release_locker(self):
        """사물함 해제"""
        if self.locker_number:
            from apps.lockers.models import Locker
            try:
                locker = Locker.objects.get(number=self.locker_number)
                released_number = self.locker_number
                locker.release()
                self.locker_number = None
                self.save()
                return released_number
            except Locker.DoesNotExist:
                pass
        
        raise Exception("해제할 사물함이 없습니다.")
    
    def auto_grade_update(self):
        """
        학년 자동 업데이트 (매년 실행)
        첫등원일 기준으로 1년마다 학년 증가
        """
        if self.grade >= 3:  # 이미 3학년이면 졸업 처리
            self.status = 'graduated'
            self.withdrawal_date = timezone.now().date()
        elif self.grade > 0:  # 고등학생인 경우만
            years_passed = (timezone.now().date() - self.first_attendance_date).days // 365
            new_grade = min(self.grade + years_passed, 3)
            if new_grade != self.grade:
                self.grade = new_grade
    
    @property
    def is_active(self):
        """재원생 여부"""
        return self.status == 'active'
    
    @property
    def attendance_days(self):
        """총 등원 일수 (개략적 계산)"""
        if self.withdrawal_date:
            return (self.withdrawal_date - self.first_attendance_date).days
        else:
            return (timezone.now().date() - self.first_attendance_date).days
    
    @property
    def grade_display(self):
        """학년 표시용"""
        return dict(self.GRADE_CHOICES)[self.grade]
    
    @property
    def status_display(self):
        """상태 표시용"""
        return dict(self.STATUS_CHOICES)[self.status]

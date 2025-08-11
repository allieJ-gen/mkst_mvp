from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Student

class StudentSerializer(serializers.ModelSerializer):
    """학생 정보 직렬화 클래스 - API 요청/응답용 데이터 변환"""
    
    # 읽기 전용 필드들 (자동 생성되는 값들)
    attendance_number = serializers.CharField(read_only=True)
    locker_number = serializers.IntegerField(read_only=True)
    created_at = serializers.DateTimeField(read_only=True)
    updated_at = serializers.DateTimeField(read_only=True)
    
    # 사용자 관련 필드들 (이름으로 표시)
    created_by_name = serializers.CharField(source='created_by.username', read_only=True)
    updated_by_name = serializers.CharField(source='updated_by.username', read_only=True)
    
    # 선택 필드들의 표시용 값
    grade_display = serializers.CharField(source='get_grade_display', read_only=True)
    gender_display = serializers.CharField(source='get_gender_display', read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    
    class Meta:
        model = Student
        fields = [
            'id',
            'attendance_number',
            'name', 
            'school',
            'grade',
            'grade_display',
            'gender',
            'gender_display',
            'locker_number',
            'first_attendance_date',
            'status',
            'status_display',
            'withdrawal_date',
            'student_phone',
            'parent_phone',
            'created_at',
            'updated_at',
            'created_by_name',
            'updated_by_name'
        ]
        
    def validate_parent_phone(self, value):
        """보호자 휴대폰번호 유효성 검사"""
        if not value:
            raise serializers.ValidationError("보호자 휴대폰번호는 필수입니다.")
        
        # 휴대폰번호 형식 검사 (010-0000-0000 또는 01000000000)
        import re
        phone_pattern = r'^010-?\d{4}-?\d{4}$'
        if not re.match(phone_pattern, value.replace('-', '')):
            raise serializers.ValidationError("올바른 휴대폰번호 형식이 아닙니다. (예: 010-1234-5678)")
        
        return value
    
    def validate_student_phone(self, value):
        """학생 휴대폰번호 유효성 검사 (선택사항)"""
        if value:  # 값이 있을 때만 검사
            import re
            phone_pattern = r'^010-?\d{4}-?\d{4}$'
            if not re.match(phone_pattern, value.replace('-', '')):
                raise serializers.ValidationError("올바른 휴대폰번호 형식이 아닙니다. (예: 010-1234-5678)")
        
        return value
    
    def validate(self, data):
        """전체 데이터 유효성 검사"""
        # 퇴원생/졸업생/강퇴생인 경우 퇴원일 필수
        if data.get('status') in ['withdrawn', 'graduated', 'expelled']:
            if not data.get('withdrawal_date'):
                raise serializers.ValidationError({
                    'withdrawal_date': '퇴원생/졸업생/강퇴생인 경우 퇴원일이 필요합니다.'
                })
        
        # 재원생인 경우 퇴원일 제거
        if data.get('status') == 'active':
            data['withdrawal_date'] = None
        
        return data

class StudentCreateSerializer(StudentSerializer):
    """학생 생성용 직렬화 클래스 - 생성 시 필요한 필드만 포함"""
    
    class Meta(StudentSerializer.Meta):
        fields = [
            'name',
            'school', 
            'grade',
            'gender',
            'first_attendance_date',
            'status',
            'withdrawal_date',
            'student_phone',
            'parent_phone'
        ]
        
class StudentListSerializer(serializers.ModelSerializer):
    """학생 목록용 간단한 직렬화 클래스 - 목록 조회 시 성능 최적화"""
    
    grade_display = serializers.CharField(source='get_grade_display', read_only=True)
    gender_display = serializers.CharField(source='get_gender_display', read_only=True) 
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    
    class Meta:
        model = Student
        fields = [
            'id',
            'attendance_number',
            'name',
            'school',
            'grade',
            'grade_display', 
            'gender',
            'gender_display',
            'status',
            'status_display',
            'locker_number',
            'first_attendance_date'
        ]

class AttendanceNumberGenerateSerializer(serializers.Serializer):
    """등원번호 생성용 직렬화 클래스"""
    
    parent_phone = serializers.CharField(
        max_length=13,
        help_text="보호자 휴대폰번호 (예: 010-1234-5678)"
    )
    
    def validate_parent_phone(self, value):
        """보호자 휴대폰번호 유효성 검사"""
        import re
        phone_pattern = r'^010-?\d{4}-?\d{4}$'
        if not re.match(phone_pattern, value.replace('-', '')):
            raise serializers.ValidationError("올바른 휴대폰번호 형식이 아닙니다. (예: 010-1234-5678)")
        
        return value


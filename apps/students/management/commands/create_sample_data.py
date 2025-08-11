from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from apps.students.models import Student
from apps.accounts.models import UserProfile
from datetime import date, timedelta
import random

class Command(BaseCommand):
    help = 'API 테스트를 위한 샘플 학생 데이터를 생성합니다.'

    def add_arguments(self, parser):
        parser.add_argument(
            '--count',
            type=int,
            default=8,
            help='생성할 학생 수 (기본값: 8명)'
        )

    def handle(self, *args, **kwargs):
        count = kwargs['count']
        
        self.stdout.write('='*50)
        self.stdout.write(self.style.SUCCESS('📊 샘플 학생 데이터 생성 시작'))
        self.stdout.write('='*50)
        
        # 샘플 데이터 템플릿
        sample_students = [
            {
                'name': '김민준',
                'school': '서현고',
                'grade': 1,
                'gender': 'M',
                'parent_phone': '010-1234-5678',
                'student_phone': '010-9876-5432',
                'status': 'active'
            },
            {
                'name': '이서연',
                'school': '분당중앙고',
                'grade': 2,
                'gender': 'F',
                'parent_phone': '010-2345-6789',
                'student_phone': '010-8765-4321',
                'status': 'active'
            },
            {
                'name': '박지훈',
                'school': '야탑고',
                'grade': 3,
                'gender': 'M',
                'parent_phone': '010-3456-7890',
                'student_phone': '',
                'status': 'active'
            },
            {
                'name': '최예은',
                'school': '서현고',
                'grade': 1,
                'gender': 'F',
                'parent_phone': '010-4567-8901',
                'student_phone': '010-6543-2109',
                'status': 'active'
            },
            {
                'name': '정현우',
                'school': '분당고',
                'grade': 2,
                'gender': 'M',
                'parent_phone': '010-5678-9012',
                'student_phone': '010-5432-1098',
                'status': 'active'
            },
            {
                'name': '한지민',
                'school': '야탑고',
                'grade': 3,
                'gender': 'F',
                'parent_phone': '010-6789-0123',
                'student_phone': '010-4321-0987',
                'status': 'withdrawn',
                'withdrawal_date': date.today() - timedelta(days=30)
            },
            {
                'name': '윤태영',
                'school': '서현고',
                'grade': 2,
                'gender': 'M',
                'parent_phone': '010-7890-1234',
                'student_phone': '',
                'status': 'active'
            },
            {
                'name': '임소영',
                'school': '분당중앙고',
                'grade': 1,
                'gender': 'F',
                'parent_phone': '010-8901-2345',
                'student_phone': '010-2109-8765',
                'status': 'graduated',
                'withdrawal_date': date.today() - timedelta(days=90)
            }
        ]
        
        # 관리자 계정 가져오기 (created_by 필드용)
        admin_user = User.objects.filter(is_superuser=True).first()
        if not admin_user:
            self.stdout.write(self.style.ERROR('❌ 관리자 계정을 찾을 수 없습니다.'))
            return
        
        created_students = []
        
        for i in range(min(count, len(sample_students))):
            student_data = sample_students[i]
            
            try:
                # 학생 생성 (등원번호는 자동 생성)
                student = Student(
                    name=student_data['name'],
                    school=student_data['school'],
                    grade=student_data['grade'],
                    gender=student_data['gender'],
                    parent_phone=student_data['parent_phone'],
                    student_phone=student_data['student_phone'],
                    status=student_data['status'],
                    first_attendance_date=date.today() - timedelta(days=random.randint(30, 365)),
                    created_by=admin_user,
                    updated_by=admin_user
                )
                
                # 퇴원/졸업생인 경우 퇴원일 설정
                if student_data['status'] in ['withdrawn', 'graduated']:
                    student.withdrawal_date = student_data.get('withdrawal_date', date.today() - timedelta(days=30))
                
                student.save()  # save() 메서드에서 등원번호 자동 생성 및 사물함 배정
                created_students.append(student)
                
                # 생성된 학생 정보 출력
                locker_info = f"사물함 {student.locker_number}번" if student.locker_number else "사물함 미배정"
                self.stdout.write(
                    f"✅ {student.name} ({student.attendance_number}) - {student.school} {student.grade}학년, {locker_info}"
                )
                
            except Exception as e:
                self.stdout.write(
                    self.style.ERROR(f"❌ {student_data['name']} 생성 실패: {str(e)}")
                )
        
        self.stdout.write('\n' + '='*50)
        self.stdout.write(self.style.SUCCESS(f'🎉 샘플 데이터 생성 완료!'))
        self.stdout.write('='*50)
        
        # 최종 통계 출력
        total_students = Student.objects.count()
        active_students = Student.objects.filter(status='active').count()
        occupied_lockers = Student.objects.filter(locker_number__isnull=False).count()
        
        self.stdout.write(f'📊 생성된 학생 수: {len(created_students)}명')
        self.stdout.write(f'📊 전체 학생 수: {total_students}명')
        self.stdout.write(f'📊 재원생 수: {active_students}명')
        self.stdout.write(f'📊 사물함 배정 수: {occupied_lockers}개')
        
        self.stdout.write('\n🔗 Django Admin에서 확인: http://127.0.0.1:8000/admin/students/student/')
        self.stdout.write(self.style.SUCCESS('샘플 데이터 생성이 완료되었습니다! 이제 API 개발을 시작할 수 있습니다.'))


from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.db import connection
from apps.students.models import Student
from apps.lockers.models import Locker
from apps.accounts.models import UserProfile
from apps.dashboard.models import DashboardStats, SystemSettings


class Command(BaseCommand):
    help = '김엄마관리형독서실 초기 데이터 설정'

    def handle(self, *args, **options):
        self.stdout.write("=== 김엄마관리형독서실 데이터베이스 연결 테스트 ===")

        # 1. 데이터베이스 연결 확인
        self.stdout.write(f"데이터베이스 연결: {connection.vendor}")
        self.stdout.write(f"데이터베이스명: {connection.settings_dict['NAME']}")
        self.stdout.write(f"사용자: {connection.settings_dict['USER']}")

        # 2. 테이블 생성 확인
        self.stdout.write("\n=== 테이블 생성 확인 ===")
        self.stdout.write(f"학생 테이블: {Student._meta.db_table}")
        self.stdout.write(f"사물함 테이블: {Locker._meta.db_table}")

        # 3. 1~271번 사물함 데이터 생성
        self.stdout.write("\n=== 사물함 데이터 초기화 ===")
        existing_lockers = Locker.objects.count()
        if existing_lockers == 0:
            self.stdout.write("271개 사물함 데이터 생성 중...")
            lockers_to_create = []
            for i in range(1, 272):  # 1~271번
                lockers_to_create.append(Locker(number=i))
            
            Locker.objects.bulk_create(lockers_to_create)
            self.stdout.write(
                self.style.SUCCESS(f"✅ {Locker.objects.count()}개 사물함 생성 완료!")
            )
        else:
            self.stdout.write(
                self.style.SUCCESS(f"✅ 기존 사물함 {existing_lockers}개 확인됨")
            )

        # 4. 관리자 계정 생성
        self.stdout.write("\n=== 관리자 계정 확인 ===")
        admin_user = User.objects.filter(username='admin').first()
        if not admin_user:
            self.stdout.write("관리자 계정 생성 중...")
            admin_user = User.objects.create_superuser(
                username='admin',
                email='admin@mkst.kr',
                password='admin123!',
                first_name='김엄마',
                last_name='관리자'
            )
            
            # UserProfile이 자동 생성되므로 역할만 설정
            admin_user.profile.role = 'ADMIN'
            admin_user.profile.department = '관리부'
            admin_user.profile.save()
            
            self.stdout.write(
                self.style.SUCCESS(f"✅ 관리자 계정 생성: {admin_user.username}")
            )
        else:
            self.stdout.write(
                self.style.SUCCESS(f"✅ 기존 관리자 계정 확인: {admin_user.username}")
            )

        # 5. 기본 시스템 설정
        self.stdout.write("\n=== 시스템 설정 초기화 ===")
        default_settings = [
            ('PAGE_SIZE', '50', 'DISPLAY', '한 페이지당 표시할 학생 수'),
            ('AUTO_BACKUP', 'true', 'BACKUP', '자동 백업 활성화'),
            ('LOCKER_COUNT', '271', 'GENERAL', '전체 사물함 개수'),
            ('SYSTEM_NAME', '김엄마관리형독서실', 'GENERAL', '시스템 이름'),
        ]

        for key, value, setting_type, description in default_settings:
            setting, created = SystemSettings.objects.get_or_create(
                key=key,
                defaults={
                    'value': value,
                    'setting_type': setting_type,
                    'description': description,
                    'updated_by': admin_user
                }
            )
            status = "생성" if created else "확인"
            self.stdout.write(f"✅ {key}: {status}")

        # 6. 통계 정보 확인
        self.stdout.write("\n=== 현재 상태 확인 ===")
        self.stdout.write(f"전체 학생 수: {Student.objects.count()}")
        self.stdout.write(f"재원생 수: {Student.objects.filter(status='ACTIVE').count()}")
        self.stdout.write(f"전체 사물함 수: {Locker.objects.count()}")
        self.stdout.write(f"사용중 사물함 수: {Locker.objects.filter(is_occupied=True).count()}")
        self.stdout.write(f"사용 가능 사물함 수: {Locker.objects.filter(is_occupied=False).count()}")

        self.stdout.write(
            self.style.SUCCESS("\n=== 초기 설정 완료 ===")
        )
        self.stdout.write("Django Admin: http://127.0.0.1:8000/admin/")
        self.stdout.write("ID: admin / PW: admin123!")
        self.stdout.write("이제 Django 개발 서버를 실행할 수 있습니다!")

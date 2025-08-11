#!/bin/bash

# 김엄마관리형독서실 학생회원관리 시스템 - macOS 설치 스크립트
# 실행 방법: bash setup_macos.sh

echo "🚀 김엄마관리형독서실 프로젝트 macOS 환경 설정 시작"
echo "=================================================="

# 1. Homebrew 설치 확인
if ! command -v brew &> /dev/null; then
    echo "📦 Homebrew 설치 중..."
    /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
else
    echo "✅ Homebrew 이미 설치됨"
fi

# 2. Python 3.11 설치
echo "🐍 Python 3.11 설치 중..."
brew install python@3.11

# 3. PostgreSQL 15 설치
echo "🐘 PostgreSQL 15 설치 중..."
brew install postgresql@15
brew services start postgresql@15

# 4. Redis 설치
echo "📦 Redis 설치 중..."
brew install redis
brew services start redis

# 5. Node.js 22 설치
echo "📦 Node.js 22 설치 중..."
brew install node@22

# 6. GitHub CLI 설치 (선택사항)
echo "📦 GitHub CLI 설치 중..."
brew install gh

# 7. 추가 도구들
echo "🛠 추가 도구 설치 중..."
brew install git

echo "=================================================="
echo "✅ 기본 설치 완료!"
echo ""
echo "📋 다음 단계:"
echo "1. git clone https://github.com/allieJ-gen/mkst_mvp.git"
echo "2. cd mkst_mvp"
echo "3. python3.11 -m venv mkst_env"
echo "4. source mkst_env/bin/activate"
echo "5. pip install -r requirements.txt"
echo "6. PostgreSQL 데이터베이스 생성 및 설정"
echo "7. python manage.py migrate"
echo "8. python manage.py createsuperuser"
echo "9. python manage.py setup_initial_data"
echo "10. python manage.py create_sample_data --count 8"
echo ""
echo "🔗 유용한 명령어:"
echo "- brew services list (실행 중인 서비스 확인)"
echo "- psql postgres (PostgreSQL 접속)"
echo "- redis-cli (Redis 접속)"
echo ""
echo "🎉 설치 완료! 이제 개발을 시작할 수 있습니다."

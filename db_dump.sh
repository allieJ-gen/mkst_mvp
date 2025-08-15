#!/bin/bash

# 김엄마관리형독서실 데이터베이스 백업 스크립트
# 작성일: 2025년 8월 11일
# 용도: 맥북 개발 환경에서 동일한 데이터베이스 상태 복원

# 색상 정의
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# 설정 변수
DB_NAME="mkst_db"
DB_USER="mkst_user"
DB_HOST="localhost"
DB_PORT="5432"
BACKUP_DIR="./database_backups"
TIMESTAMP=$(date +"%Y%m%d_%H%M%S")
BACKUP_FILE="${BACKUP_DIR}/mkst_db_backup_${TIMESTAMP}.sql"
BACKUP_FILE_COMPRESSED="${BACKUP_FILE}.gz"

echo -e "${BLUE}🗄️  김엄마관리형독서실 데이터베이스 백업 시작${NC}"
echo -e "${BLUE}📅 백업 시간: $(date)${NC}"
echo ""

# 백업 디렉토리 생성
if [ ! -d "$BACKUP_DIR" ]; then
    echo -e "${YELLOW}📁 백업 디렉토리 생성: $BACKUP_DIR${NC}"
    mkdir -p "$BACKUP_DIR"
fi

# PostgreSQL 서비스 상태 확인
echo -e "${YELLOW}🔍 PostgreSQL 서비스 상태 확인 중...${NC}"
if ! pg_isready -h $DB_HOST -p $DB_PORT -U $DB_USER -d $DB_NAME > /dev/null 2>&1; then
    echo -e "${RED}❌ PostgreSQL 서비스에 연결할 수 없습니다.${NC}"
    echo -e "${YELLOW}💡 다음 명령어로 PostgreSQL을 시작해주세요:${NC}"
    echo -e "   brew services start postgresql@15"
    exit 1
fi

echo -e "${GREEN}✅ PostgreSQL 서비스 정상 작동 중${NC}"

# 데이터베이스 존재 여부 확인
echo -e "${YELLOW}🔍 데이터베이스 존재 여부 확인 중...${NC}"
if ! psql -h $DB_HOST -p $DB_PORT -U $DB_USER -lqt | cut -d \| -f 1 | grep -qw $DB_NAME; then
    echo -e "${RED}❌ 데이터베이스 '$DB_NAME'이 존재하지 않습니다.${NC}"
    echo -e "${YELLOW}💡 다음 명령어로 데이터베이스를 생성해주세요:${NC}"
    echo -e "   psql -U $DB_USER -f setup_db.sql"
    exit 1
fi

echo -e "${GREEN}✅ 데이터베이스 '$DB_NAME' 확인됨${NC}"

# 백업 시작
echo -e "${YELLOW}📦 데이터베이스 백업 시작...${NC}"
echo -e "${BLUE}📁 백업 파일: $BACKUP_FILE${NC}"

# pg_dump 실행 (스키마 + 데이터 + 권한 포함)
if pg_dump -h $DB_HOST -p $DB_PORT -U $DB_USER \
    --verbose \
    --clean \
    --create \
    --if-exists \
    --no-owner \
    --no-privileges \
    --schema=public \
    --file="$BACKUP_FILE" \
    $DB_NAME; then
    
    echo -e "${GREEN}✅ 데이터베이스 백업 완료!${NC}"
    
    # 백업 파일 크기 확인
    BACKUP_SIZE=$(du -h "$BACKUP_FILE" | cut -f1)
    echo -e "${BLUE}📊 백업 파일 크기: $BACKUP_SIZE${NC}"
    
    # 압축
    echo -e "${YELLOW}🗜️  백업 파일 압축 중...${NC}"
    if gzip "$BACKUP_FILE"; then
        echo -e "${GREEN}✅ 압축 완료: $BACKUP_FILE_COMPRESSED${NC}"
        COMPRESSED_SIZE=$(du -h "$BACKUP_FILE_COMPRESSED" | cut -f1)
        echo -e "${BLUE}📊 압축 후 크기: $COMPRESSED_SIZE${NC}"
        
        # 압축 전 파일 삭제
        rm -f "$BACKUP_FILE"
        echo -e "${YELLOW}🗑️  압축 전 파일 삭제됨${NC}"
    else
        echo -e "${RED}❌ 압축 실패${NC}"
    fi
    
    # 백업 파일 정보 출력
    echo ""
    echo -e "${GREEN}🎉 백업 완료 요약${NC}"
    echo -e "${BLUE}📁 백업 파일: $BACKUP_FILE_COMPRESSED${NC}"
    echo -e "${BLUE}📊 파일 크기: $COMPRESSED_SIZE${NC}"
    echo -e "${BLUE}📅 백업 시간: $(date)${NC}"
    echo ""
    echo -e "${YELLOW}💡 맥북에서 복원하는 방법:${NC}"
    echo -e "   1. 이 파일을 맥북으로 복사"
    echo -e "   2. PostgreSQL 설치 및 데이터베이스 생성"
    echo -e "   3. 다음 명령어로 복원:"
    echo -e "      gunzip -c $BACKUP_FILE_COMPRESSED | psql -U mkst_user -d mkst_db"
    echo ""
    echo -e "${GREEN}✅ 백업 스크립트 실행 완료!${NC}"
    
else
    echo -e "${RED}❌ 데이터베이스 백업 실패${NC}"
    echo -e "${YELLOW}💡 오류 내용을 확인해주세요.${NC}"
    exit 1
fi

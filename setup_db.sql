-- 김엄마관리형독서실 데이터베이스 설정 스크립트

-- 1. 데이터베이스 사용자 생성
CREATE USER mkst_user WITH PASSWORD 'mkst_password';

-- 2. 데이터베이스 생성
CREATE DATABASE mkst_db WITH 
    OWNER = mkst_user
    ENCODING = 'UTF8'
    LC_COLLATE = 'ko_KR.UTF-8'
    LC_CTYPE = 'ko_KR.UTF-8'
    TEMPLATE = template0;

-- 3. 사용자 권한 부여
GRANT ALL PRIVILEGES ON DATABASE mkst_db TO mkst_user;

-- 4. 연결 확인
\c mkst_db mkst_user

-- 5. 스키마 권한 부여 (Django가 테이블 생성할 수 있도록)
GRANT ALL ON SCHEMA public TO mkst_user;
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO mkst_user;
GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO mkst_user;

-- 6. 기본 권한 설정 (새로 생성되는 객체에 대해)
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL ON TABLES TO mkst_user;
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL ON SEQUENCES TO mkst_user;

-- 설정 완료 메시지
\echo '============================================='
\echo '김엄마관리형독서실 데이터베이스 설정 완료!'
\echo '데이터베이스: mkst_db'
\echo '사용자: mkst_user'
\echo '============================================='

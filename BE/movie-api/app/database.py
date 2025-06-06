import os
from sqlalchemy import create_engine # SQLAlchemy를 사용하여 PostgreSQL 데이터베이스와 연결하기 위한 설정
from sqlalchemy.ext.declarative import declarative_base # 데이터베이스 모델의 베이스 클래스
from sqlalchemy.orm import sessionmaker 

# 1) 환경변수에서 DATABASE_URL 읽기
DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL:
    raise RuntimeError("DATABASE_URL 환경변수가 설정되지 않았습니다.")

# 2) Postgre용 엔진 생성
engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,      # 커넥션이 끊겨도 자동 복구
    pool_recycle=3600        # 장시간 유휴 시 재생성
)

# 3) 세션 팩토리
SessionLocal = sessionmaker( #
    autocommit=False, # 자동 커밋 비활성화
    autoflush=False, # 자동 플러시 비활성화
    bind=engine, # 엔진 바인딩
)

# 4) 베이스 클래스
Base = declarative_base()
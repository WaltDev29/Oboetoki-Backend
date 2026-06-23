import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from dotenv import load_dotenv

# 환경변수 로드
load_dotenv()

# docker-compose로 구동 시 환경 변수 DB_URL 사용
DB_URL = os.environ.get("DB_URL", "mysql+pymysql://oboetoki_user:oboetoki_password@localhost:3306/oboetoki")

engine = create_engine(DB_URL, echo=False)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# 의존성 주입을 위한 DB 세션 생성 함수
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

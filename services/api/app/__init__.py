from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .db.database import Base, engine
from .routes import auth, words, main as main_route

def create_app() -> FastAPI:
    # 데이터베이스 테이블 생성
    Base.metadata.create_all(bind=engine)

    tags_metadata = [
        {"name": "Auth", "description": "사용자 인증 및 회원가입 관련 API"},
        {"name": "Words", "description": "사용자 개인 단어장 관리 및 OCR 스캔 API"},
        {"name": "Main", "description": "앱 메인 화면용 통계 및 데이터 조회 API"}
    ]

    app = FastAPI(
        title="Oboetoki API",
        description="Oboetoki 안드로이드 앱을 위한 백엔드 API",
        version="1.0.0",
        openapi_tags=tags_metadata
    )

    # CORS 설정 (앱에서의 접근 허용)
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # 라우터 등록
    app.include_router(auth.router, prefix="/auth", tags=["Auth"])
    app.include_router(words.router, prefix="/words", tags=["Words"])
    app.include_router(main_route.router, prefix="/main", tags=["Main"])

    return app

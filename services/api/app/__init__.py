from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .db.database import Base, engine
from .routes import auth, words, main as main_route

def create_app() -> FastAPI:
    # 데이터베이스 테이블 생성
    Base.metadata.create_all(bind=engine)

    app = FastAPI(
        title="Oboetoki API",
        description="Oboetoki 안드로이드 앱을 위한 백엔드 API",
        version="1.0.0",
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

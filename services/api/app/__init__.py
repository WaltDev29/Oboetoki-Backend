from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .db.database import Base, engine
from .routes import auth, words, main as main_route
from .models.quote import Quote
from .db.database import SessionLocal

def create_app() -> FastAPI:
    # 데이터베이스 테이블 생성
    Base.metadata.create_all(bind=engine)
    
    # 명언 초기 데이터 삽입
    db = SessionLocal()
    try:
        if db.query(Quote).count() == 0:
            initial_quotes = [
                Quote(text="꾸준함이 모든 것을 이깁니다. 오늘도 파이팅!"),
                Quote(text="오늘 걷지 않으면 내일은 뛰어야 합니다."),
                Quote(text="작은 성취가 모여 큰 성공을 만듭니다."),
                Quote(text="시작이 반이다. 지금 바로 단어 하나를 더 외워보세요."),
                Quote(text="실패는 성공의 어머니입니다. 틀린 단어는 다시 보면 됩니다."),
                Quote(text="외국어 학습의 왕도는 반복입니다."),
                Quote(text="매일 조금씩 성장하는 자신을 믿으세요.")
            ]
            db.add_all(initial_quotes)
            db.commit()
    finally:
        db.close()

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

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from ..db.database import get_db
from ..models.user import User
from ..schemas.user import UserCreate, UserResponse, Token
from ..core.security import get_password_hash, verify_password, create_access_token, ACCESS_TOKEN_EXPIRE_MINUTES
from datetime import timedelta

router = APIRouter()

@router.post(
    "/signup", 
    response_model=UserResponse,
    summary="회원가입",
    description="이메일, 비밀번호, 이름, 전화번호를 입력받아 새로운 사용자를 생성합니다."
)
def signup(user: UserCreate, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.email == user.email).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    hashed_password = get_password_hash(user.password)
    new_user = User(
        email=user.email,
        password_hash=hashed_password,
        name=user.name,
        phone=user.phone
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@router.get(
    "/check-email",
    summary="이메일 중복 확인",
    description="입력한 이메일이 이미 가입되어 있는지 확인합니다. 사용 가능하면 true를 반환합니다."
)
def check_email(email: str, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == email).first()
    if user:
        return {"is_available": False}
    return {"is_available": True}

@router.post(
    "/login", 
    response_model=Token,
    summary="로그인 (토큰 발급)",
    description="이메일과 비밀번호로 로그인하여 JWT 액세스 토큰을 발급받습니다."
)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    # OAuth2PasswordRequestForm은 기본적으로 username 필드를 사용하므로, 클라이언트가 이메일을 username 필드에 담아 보냅니다.
    user = db.query(User).filter(User.email == form_data.username).first()
    if not user or not verify_password(form_data.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

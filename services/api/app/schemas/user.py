from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import date

class UserCreate(BaseModel):
    email: EmailStr = Field(..., examples=["user@example.com"], description="사용자 이메일 주소 (로그인 아이디로 사용)")
    password: str = Field(..., examples=["securepassword123!"], description="비밀번호 (서버에 해시되어 저장됨)")
    name: str = Field(..., examples=["홍길동"], description="사용자 이름 또는 닉네임")
    phone: str = Field(..., examples=["010-1234-5678"], description="사용자 전화번호")

class UserResponse(BaseModel):
    id: int = Field(..., examples=[1])
    email: str = Field(..., examples=["user@example.com"])
    name: str = Field(..., examples=["홍길동"])
    phone: str = Field(..., examples=["010-1234-5678"])
    consecutive_attendance: int = Field(..., examples=[3], description="연속 출석 일수")
    last_login_date: Optional[date] = Field(None, examples=["2024-01-01"], description="마지막 로그인 일자")
    
    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str

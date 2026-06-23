from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import date

class UserCreate(BaseModel):
    username: str
    password: str
    name: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[EmailStr] = None

class UserResponse(BaseModel):
    id: int
    username: str
    name: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[str] = None
    consecutive_attendance: int
    last_login_date: Optional[date] = None

    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str

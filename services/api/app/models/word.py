from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey
from sqlalchemy.sql import func
from ..db.database import Base

class UserWord(Base):
    __tablename__ = "user_words"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    original_word = Column(String(255), nullable=False)
    reading = Column(String(255), nullable=True) # 일본어 요미가나, 발음 기호 등
    translated_word = Column(String(255), nullable=False)
    source_language = Column(String(10), nullable=True) # 예: 'en', 'ja', 'ko' 등
    is_memorized = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime

class WordCreate(BaseModel):
    original_word: str = Field(..., examples=["暮らす"], description="추출된 원어")
    reading: Optional[str] = Field(None, examples=["くらす"], description="원어의 발음 (예: 일본어 요미가나)")
    translated_word: str = Field(..., examples=["살다, 생활하다"], description="파싱된 한국어 뜻")
    source_language: Optional[str] = Field(None, examples=["ja"], description="원본 언어 코드 (en, ko, ja, ...)")

class WordUpdate(BaseModel):
    original_word: Optional[str] = Field(None, examples=["暮らす"])
    reading: Optional[str] = Field(None, examples=["くらす"])
    translated_word: Optional[str] = Field(None, examples=["살아 가다"])
    is_memorized: Optional[bool] = Field(None, examples=[True], description="암기 완료 여부 체크")

class WordResponse(BaseModel):
    id: int = Field(..., examples=[10])
    user_id: int = Field(..., examples=[1])
    original_word: str = Field(..., examples=["暮らす"])
    reading: Optional[str] = Field(None, examples=["くらす"])
    translated_word: str = Field(..., examples=["살다, 생활하다"])
    source_language: Optional[str] = Field(None, examples=["ja"])
    is_memorized: bool = Field(..., examples=[False])
    created_at: datetime = Field(..., examples=["2024-01-01T12:00:00Z"])

    class Config:
        from_attributes = True

class OCRParsedWord(BaseModel):
    original: str = Field(..., examples=["暮らす"])
    reading: Optional[str] = Field(None, examples=["くらす"])
    translated: str = Field(..., examples=["살다, 생활하다"])
    source_language: str = Field(..., examples=["ja"])

class OCRResponse(BaseModel):
    parsed_words: List[OCRParsedWord]

class BatchWordResponse(BaseModel):
    added_words: List[WordResponse] = Field(..., description="성공적으로 추가된 단어 목록")
    ignored_words: List[str] = Field(..., description="이미 존재하여 추가가 무시된 단어들의 원어 목록")

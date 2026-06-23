from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

class WordCreate(BaseModel):
    original_word: str
    translated_word: str
    source_language: Optional[str] = None

class WordUpdate(BaseModel):
    original_word: Optional[str] = None
    translated_word: Optional[str] = None
    is_memorized: Optional[bool] = None
    memorization_level: Optional[int] = None

class WordResponse(BaseModel):
    id: int
    user_id: int
    original_word: str
    translated_word: str
    source_language: Optional[str] = None
    is_memorized: bool
    memorization_level: int
    created_at: datetime

    class Config:
        from_attributes = True

class OCRParsedWord(BaseModel):
    original: str
    translated: str

class OCRResponse(BaseModel):
    parsed_words: List[OCRParsedWord]

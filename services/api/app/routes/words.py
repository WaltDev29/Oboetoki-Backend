from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from sqlalchemy.orm import Session
from typing import List, Optional
from ..db.database import get_db
from ..models.user import User
from ..models.word import UserWord
from ..schemas.word import WordCreate, WordUpdate, WordResponse, OCRResponse, OCRParsedWord
from ..core.security import get_current_user
from ..services.llm_service import parse_image_to_words

router = APIRouter()

@router.get("/", response_model=List[WordResponse])
def get_words(
    is_memorized: Optional[bool] = None,
    sort_by: str = "created_at", # "created_at" or "memorization_level"
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    query = db.query(UserWord).filter(UserWord.user_id == current_user.id)
    
    if is_memorized is not None:
        query = query.filter(UserWord.is_memorized == is_memorized)
        
    if sort_by == "memorization_level":
        query = query.order_by(UserWord.memorization_level.desc())
    else:
        query = query.order_by(UserWord.created_at.desc())
        
    return query.all()

@router.post("/", response_model=WordResponse)
def create_word(word: WordCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    new_word = UserWord(
        user_id=current_user.id,
        original_word=word.original_word,
        translated_word=word.translated_word,
        source_language=word.source_language
    )
    db.add(new_word)
    db.commit()
    db.refresh(new_word)
    return new_word

@router.post("/batch", response_model=List[WordResponse])
def create_words_batch(words: List[WordCreate], db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    new_words = []
    for w in words:
        new_word = UserWord(
            user_id=current_user.id,
            original_word=w.original_word,
            translated_word=w.translated_word,
            source_language=w.source_language
        )
        new_words.append(new_word)
        db.add(new_word)
    
    db.commit()
    for w in new_words:
        db.refresh(w)
    return new_words

@router.get("/{word_id}", response_model=WordResponse)
def get_word(word_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    word = db.query(UserWord).filter(UserWord.id == word_id, UserWord.user_id == current_user.id).first()
    if not word:
        raise HTTPException(status_code=404, detail="Word not found")
    return word

@router.put("/{word_id}", response_model=WordResponse)
def update_word(word_id: int, word_update: WordUpdate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    word = db.query(UserWord).filter(UserWord.id == word_id, UserWord.user_id == current_user.id).first()
    if not word:
        raise HTTPException(status_code=404, detail="Word not found")
    
    if word_update.original_word is not None:
        word.original_word = word_update.original_word
    if word_update.translated_word is not None:
        word.translated_word = word_update.translated_word
    if word_update.is_memorized is not None:
        word.is_memorized = word_update.is_memorized
    if word_update.memorization_level is not None:
        word.memorization_level = word_update.memorization_level
        
    db.commit()
    db.refresh(word)
    return word

@router.post("/ocr", response_model=OCRResponse)
async def process_ocr_image(file: UploadFile = File(...), current_user: User = Depends(get_current_user)):
    """
    이미지를 업로드받아 OpenAI Vision API를 통해 직접 단어와 뜻을 추출하여 파싱해 반환합니다.
    """
    contents = await file.read()
    
    parsed_data = parse_image_to_words(contents)
    
    # Dict List -> Pydantic Model List
    parsed_words = []
    for item in parsed_data:
        if "original" in item and "translated" in item:
            parsed_words.append(OCRParsedWord(original=item["original"], translated=item["translated"]))
            
    return OCRResponse(parsed_words=parsed_words)

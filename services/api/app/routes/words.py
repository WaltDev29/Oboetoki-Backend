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

@router.get(
    "/", 
    response_model=List[WordResponse],
    summary="내 단어장 목록 조회",
    description="현재 로그인한 사용자의 단어장 목록을 불러옵니다. `is_memorized` 파라미터로 암기 완료 여부를 필터링할 수 있습니다."
)
def get_words(
    is_memorized: Optional[bool] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    query = db.query(UserWord).filter(UserWord.user_id == current_user.id)
    
    if is_memorized is not None:
        query = query.filter(UserWord.is_memorized == is_memorized)
        
    query = query.order_by(UserWord.created_at.desc())
        
    return query.all()

@router.post(
    "/", 
    response_model=WordResponse,
    summary="단일 단어 추가",
    description="사용자의 단어장에 새로운 단어를 하나 추가합니다."
)
def create_word(word: WordCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    new_word = UserWord(
        user_id=current_user.id,
        original_word=word.original_word,
        reading=word.reading,
        translated_word=word.translated_word,
        source_language=word.source_language
    )
    db.add(new_word)
    db.commit()
    db.refresh(new_word)
    return new_word

@router.post(
    "/batch", 
    response_model=List[WordResponse],
    summary="여러 단어 한 번에 추가",
    description="배열 형태로 여러 개의 단어를 한 번에 추가합니다. (주로 OCR 파싱 결과를 한꺼번에 저장할 때 사용)"
)
def create_words_batch(words: List[WordCreate], db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    new_words = []
    for w in words:
        new_word = UserWord(
            user_id=current_user.id,
            original_word=w.original_word,
            reading=w.reading,
            translated_word=w.translated_word,
            source_language=w.source_language
        )
        new_words.append(new_word)
        db.add(new_word)
    
    db.commit()
    for w in new_words:
        db.refresh(w)
    return new_words

@router.get(
    "/{word_id}", 
    response_model=WordResponse,
    summary="특정 단어 상세 조회",
    description="단어 ID를 통해 특정 단어의 상세 정보를 조회합니다."
)
def get_word(word_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    word = db.query(UserWord).filter(UserWord.id == word_id, UserWord.user_id == current_user.id).first()
    if not word:
        raise HTTPException(status_code=404, detail="Word not found")
    return word

@router.put(
    "/{word_id}", 
    response_model=WordResponse,
    summary="특정 단어 정보 수정",
    description="단어의 원어, 발음, 뜻, 암기 여부 등을 수정합니다."
)
def update_word(word_id: int, word_update: WordUpdate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    word = db.query(UserWord).filter(UserWord.id == word_id, UserWord.user_id == current_user.id).first()
    if not word:
        raise HTTPException(status_code=404, detail="Word not found")
    
    if word_update.original_word is not None:
        word.original_word = word_update.original_word
    if word_update.reading is not None:
        word.reading = word_update.reading
    if word_update.translated_word is not None:
        word.translated_word = word_update.translated_word
    if word_update.is_memorized is not None:
        word.is_memorized = word_update.is_memorized
        
    db.commit()
    db.refresh(word)
    return word

@router.post(
    "/ocr", 
    response_model=OCRResponse,
    summary="단어장 이미지 OCR 및 의미 추출",
    description="사진(이미지)을 업로드받아 LLM 모델을 통해 원어, 발음, 한국어 뜻, 원본 언어 코드를 한 번에 추출합니다."
)
async def process_ocr_image(file: UploadFile = File(...), current_user: User = Depends(get_current_user)):
    """
    이미지를 업로드받아 LLM API를 통해 직접 단어와 뜻을 추출하여 파싱해 반환합니다.
    """
    contents = await file.read()
    
    parsed_data = parse_image_to_words(contents)
    
    # Dict List -> Pydantic Model List
    parsed_words = []
    for item in parsed_data:
        if "original" in item and "translated" in item and "source_language" in item:
            parsed_words.append(OCRParsedWord(
                original=item["original"], 
                reading=item.get("reading"),
                translated=item["translated"],
                source_language=item["source_language"]
            ))
            
    return OCRResponse(parsed_words=parsed_words)

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from datetime import datetime, date, timedelta
from zoneinfo import ZoneInfo
from ..db.database import get_db
from ..models.user import User
from ..models.word import UserWord
from ..core.security import get_current_user
from ..services.quote_service import get_daily_quote
router = APIRouter()

def get_kst_today() -> date:
    return datetime.now(ZoneInfo("Asia/Seoul")).date()

@router.get("/")
def get_main_page_data(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    today = get_kst_today()
    
    # 출석 체크 로직
    if current_user.last_login_date != today:
        if current_user.last_login_date == today - timedelta(days=1):
            current_user.consecutive_attendance += 1
        else:
            current_user.consecutive_attendance = 1
        current_user.last_login_date = today
        db.commit()
        db.refresh(current_user)
        
    # 단어 통계
    total_words = db.query(UserWord).filter(UserWord.user_id == current_user.id).count()
    memorized_words = db.query(UserWord).filter(UserWord.user_id == current_user.id, UserWord.is_memorized == True).count()
    
    # 명언 생성 (서비스 분리)
    quote = get_daily_quote(db, today)
    
    return {
        "consecutive_attendance": current_user.consecutive_attendance,
        "total_words": total_words,
        "memorized_words": memorized_words,
        "quote_of_the_day": quote
    }

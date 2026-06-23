from sqlalchemy.orm import Session
from datetime import date
from ..models.quote import Quote

def get_daily_quote(db: Session, target_date: date) -> str:
    """
    주어진 날짜(target_date)에 맞는 일일 명언을 반환합니다.
    (하루 동안은 항상 같은 명언을 반환하도록 설계)
    """
    total_quotes = db.query(Quote).count()
    if total_quotes > 0:
        day_of_year = target_date.timetuple().tm_yday
        quote_index = day_of_year % total_quotes
        quote_obj = db.query(Quote).offset(quote_index).first()
        return quote_obj.text if quote_obj else "오늘도 파이팅!"
    return "오늘도 파이팅!"

from sqlalchemy import Column, Integer, String, Date
from ..db.database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(100), unique=True, index=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    name = Column(String(50), nullable=False)
    phone = Column(String(20), nullable=False)
    last_login_date = Column(Date, nullable=True)
    consecutive_attendance = Column(Integer, default=0)

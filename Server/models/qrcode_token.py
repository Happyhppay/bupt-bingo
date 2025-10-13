from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Boolean
from sqlalchemy.sql import func
from database import Base


class QrcodeToken(Base):
    __tablename__ = "qrcode_token"

    id = Column(Integer, primary_key=True, index=True)
    token = Column(String(64), unique=True, index=True, nullable=False)
    club_id = Column(Integer, ForeignKey("club.id"), nullable=False)
    is_used = Column(Integer, default=0)  # 0-未使用，1-已使用
    expire_time = Column(DateTime(timezone=True))
    create_time = Column(DateTime(timezone=True), default=func.now())

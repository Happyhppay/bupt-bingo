from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.sql import func
from database import Base


class AwardToken(Base):
    __tablename__ = "award_token"

    id = Column(Integer, primary_key=True, index=True)
    token = Column(String(64), unique=True, index=True, nullable=False)
    user_id = Column(Integer, ForeignKey("user.id"), nullable=False)
    reward = Column(Integer, nullable=False)
    is_verified = Column(Integer, default=0)  # 0-未验证，1-已验证
    create_time = Column(DateTime(timezone=True), default=func.now())
    verify_time = Column(DateTime(timezone=True))

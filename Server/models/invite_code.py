from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.sql import func
from database import Base


class InviteCode(Base):
    __tablename__ = "invite_code"

    id = Column(Integer, primary_key=True, index=True)
    code = Column(String(16), unique=True, index=True, nullable=False)
    role = Column(Integer, nullable=False)  # 1-社团成员，2-管理员
    club_id = Column(Integer, ForeignKey("club.id"), nullable=True)
    is_used = Column(Integer, default=0)  # 0-未使用，1-已使用
    create_time = Column(DateTime(timezone=True), default=func.now())
    use_time = Column(DateTime(timezone=True))

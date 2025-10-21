from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Boolean
from sqlalchemy.sql import func
from database import Base


class User(Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True, index=True)  # 学号
    points = Column(Integer, default=0)
    special_points = Column(Integer, default=0)
    bingo = Column(Integer, default=0)
    role = Column(Integer, default=0)  # 0-普通用户，1-社团成员，2-管理员
    club_id = Column(Integer, ForeignKey("club.id"), nullable=True, default=None)
    first_entry_time = Column(DateTime(timezone=True), default=func.now())
    update_time = Column(DateTime(timezone=True), default=func.now(), onupdate=func.now())

from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Boolean
from sqlalchemy.sql import func
from database import Base

class UserScan(Base):
    __tablename__ = "user_scan"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("user.id"), nullable=False)
    club_id = Column(Integer, ForeignKey("club.id"), nullable=False)
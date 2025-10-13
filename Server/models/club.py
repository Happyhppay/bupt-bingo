from sqlalchemy import Column, Integer, String
from database import Base


class Club(Base):
    __tablename__ = "club"

    id = Column(Integer, primary_key=True, index=True)
    club_name = Column(String(32), unique=True, index=True, nullable=False)
    club_type = Column(Integer, default=0)  # 0-一般社团，1-特殊社团

# models.py
from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship
from database import Base
from datetime import datetime

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String, unique=True, index=True)
    nickname = Column(String)
    avatar = Column(String)
    first_enter_time = Column(DateTime, default=datetime.utcnow)
    role = Column(String, default="normal")  # normal, club, admin
    point = Column(Integer, default=0)
    special_point = Column(Integer, default=0)

    scans = relationship("ScanRecord", back_populates="user")
    rewards = relationship("RewardToken", back_populates="user")

class Club(Base):
    __tablename__ = "clubs"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    qrcode_token = Column(String, unique=True)  # 当前有效 token
    last_refresh = Column(DateTime, default=datetime.utcnow)

class ScanRecord(Base):
    __tablename__ = "scan_records"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    club_name = Column(String)
    scan_time = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="scans")

class BingoGrid(Base):
    __tablename__ = "bingo_grids"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), unique=True)
    grid_data = Column(Text)  # JSON string: 5x5 list of 0/1
    updated_at = Column(DateTime, default=datetime.utcnow)

class InviteCode(Base):
    __tablename__ = "invite_codes"

    id = Column(Integer, primary_key=True, index=True)
    code = Column(String, unique=True)
    role = Column(String)  # club, admin
    club_name = Column(String, nullable=True)

class QrcodeToken(Base):
    __tablename__ = "qrcode_tokens"

    id = Column(Integer, primary_key=True, index=True)
    token = Column(String, unique=True)
    club_name = Column(String)
    used = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)

class RewardToken(Base):
    __tablename__ = "reward_tokens"

    id = Column(Integer, primary_key=True, index=True)
    token = Column(String, unique=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    bingo_type = Column(String)
    claimed = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    claimed_at = Column(DateTime, nullable=True)

    user = relationship("User", back_populates="rewards")
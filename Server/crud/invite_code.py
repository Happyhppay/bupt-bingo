from sqlalchemy.orm import Session
from models.invite_code import InviteCode
from schemas.invite import InviteCodeCreate, InviteCodeUpdate
from datetime import datetime

def get_invite_code(db: Session, code: str):
    return db.query(InviteCode).filter(InviteCode.code == code).first()

def get_invite_codes(db: Session, skip: int = 0, limit: int = 100):
    return db.query(InviteCode).offset(skip).limit(limit).all()

def create_invite_code(db: Session, invite_code: InviteCodeCreate):
    db_code = InviteCode(
        code=invite_code.code,
        role=invite_code.role,
        club_id=invite_code.club_id,
        is_used=0
    )
    db.add(db_code)
    db.commit()
    db.refresh(db_code)
    return db_code

def update_invite_code_status(db: Session, code_id: int, is_used: int = 1):
    db_code = db.query(InviteCode).filter(InviteCode.id == code_id).first()
    if db_code:
        db_code.is_used = is_used
        db_code.use_time = datetime.now()
        db.commit()
        db.refresh(db_code)
    return db_code

def get_valid_unused_invite_code(db: Session, code: str):
    """获取有效的未使用邀请码"""
    return db.query(InviteCode).filter(
        InviteCode.code == code,
        InviteCode.is_used == 0
    ).first()

from sqlalchemy.orm import Session
from models.qrcode_token import QrcodeToken
from datetime import datetime, timedelta

def get_qrcode_token(db: Session, token: str):
    return db.query(QrcodeToken).filter(QrcodeToken.token == token).first()

def get_qrcode_tokens_by_club(db: Session, club_id: int, skip: int = 0, limit: int = 100):
    return db.query(QrcodeToken).filter(QrcodeToken.club_id == club_id).offset(skip).limit(limit).all()

def create_qrcode_token(db: Session, token: str, club_id: int, expire_minutes: int = 5):
    expire_time = datetime.now() + timedelta(minutes=expire_minutes)
    db_token = QrcodeToken(
        token=token,
        club_id=club_id,
        is_used=0,
        expire_time=expire_time
    )
    db.add(db_token)
    db.commit()
    db.refresh(db_token)
    return db_token

def update_qrcode_token_status(db: Session, token_id: int, is_used: int = 1):
    db_token = db.query(QrcodeToken).filter(QrcodeToken.id == token_id).first()
    if db_token:
        db_token.is_used = is_used
        db.commit()
        db.refresh(db_token)
    return db_token

def get_valid_unused_token(db: Session, token: str):
    """获取有效的未使用token"""
    now = datetime.now()
    return db.query(QrcodeToken).filter(
        QrcodeToken.token == token,
        QrcodeToken.is_used == 0,
        QrcodeToken.expire_time > now
    ).first()

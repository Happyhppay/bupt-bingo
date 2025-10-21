from sqlalchemy.orm import Session
from models.award_token import AwardToken
from datetime import datetime


def get_award_token(db: Session, token: str):
    return db.query(AwardToken).filter(AwardToken.token == token).first()


def get_award_tokens_by_user(db: Session, user_id: int, limit: int = 100):
    return db.query(AwardToken).filter(AwardToken.user_id == user_id).limit(limit).all()


def create_award_token(db: Session, token: str, user_id: int, reward: int):
    db_token = AwardToken(
        token=token,
        user_id=user_id,
        reward=reward,
        is_verified=0
    )
    db.add(db_token)
    db.commit()
    db.refresh(db_token)
    return db_token


def verify_award_token(db: Session, token_id: int):
    db_token = db.query(AwardToken).filter(AwardToken.id == token_id).first()
    if db_token:
        db_token.is_verified = 1
        db_token.verify_time = datetime.now()
        db.commit()
        db.refresh(db_token)
    return db_token


def has_verified_award(db: Session, user_id: int, bingo_level: int) -> bool:
    """检查用户是否已经对指定奖励等级完成验证（领取）。"""
    existing = db.query(AwardToken).filter(
        AwardToken.user_id == user_id,
        AwardToken.bingo == bingo_level,
        AwardToken.is_verified == 1
    ).first()
    return existing is not None

from sqlalchemy.orm import Session
from models.award_token import AwardToken
from schemas.reward import AwardTokenCreate
from datetime import datetime

def get_award_token(db: Session, token: str):
    return db.query(AwardToken).filter(AwardToken.token == token).first()

def get_award_tokens_by_user(db: Session, user_id: int, skip: int = 0, limit: int = 100):
    return db.query(AwardToken).filter(AwardToken.user_id == user_id).offset(skip).limit(limit).all()

def create_award_token(db: Session, award_token: AwardTokenCreate):
    db_token = AwardToken(
        token=award_token.token,
        user_id=award_token.user_id,
        bingo=award_token.reward_level,
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

from sqlalchemy.orm import Session
from models.award_token import AwardToken
from schemas.reward import AwardTokenCreate
from datetime import datetime
from typing import Union, Dict, Any


def get_award_token(db: Session, token: str):
    return db.query(AwardToken).filter(AwardToken.token == token).first()


def get_award_tokens_by_user(db: Session, user_id: int, skip: int = 0, limit: int = 100):
    return db.query(AwardToken).filter(AwardToken.user_id == user_id).offset(skip).limit(limit).all()


def create_award_token(db: Session, award_token: Union[AwardTokenCreate, Dict[str, Any]]):
    """
    创建领奖记录。支持传入 pydantic 对象或普通 dict（兼容 api/reward.py 传入的 dict）。
    支持的 dict 字段： token, user_id, bingo 或 reward_level
    """
    # 兼容不同来源的数据结构
    if isinstance(award_token, dict):
        token_val = award_token.get('token')
        user_id_val = award_token.get('user_id')
        # 优先支持 bingo 字段（部分代码使用 bingo），否则尝试 reward_level
        bingo_val = award_token.get('bingo', award_token.get('reward_level'))
    else:
        token_val = getattr(award_token, 'token', None)
        user_id_val = getattr(award_token, 'user_id', None)
        bingo_val = getattr(award_token, 'reward_level', None)

    db_token = AwardToken(
        token=token_val,
        user_id=user_id_val,
        bingo=bingo_val,
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

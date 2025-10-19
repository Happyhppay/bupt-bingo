from sqlalchemy.orm import Session
from models.user import User
from datetime import datetime
from typing import Optional

def get_user(db: Session, user_id: int):
    """根据ID获取用户"""
    return db.query(User).filter(User.id == user_id).first()

def get_user_by_student_id_and_name(db: Session, student_id: int, name: str):
    """根据学号和姓名获取用户"""
    return db.query(User).filter(User.id == student_id, User.name == name).first()

def create_user(db: Session, student_id: int, name: str):
    """创建新用户"""
    db_user = User(
        id=student_id,
        name=name,
        points=0,
        special_points=0,
        role=0,
        club_id=None
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def update_user_role(db: Session, user_id: int, role: int, club_id: Optional[int] = None):
    """更新用户角色"""
    db_user = db.query(User).filter(User.id == user_id).first()
    if db_user:
        db_user.role = role
        if role == 1:  # 社团成员
            db_user.club_id = club_id
        else:  # 管理员或普通用户
            db_user.club_id = None
        db_user.update_time = datetime.now()
        db.commit()
        db.refresh(db_user)
    return db_user

def update_user_points(db: Session, user_id: int, add_points: int = 0, add_special: int = 0):
    """更新用户积分"""
    db_user = db.query(User).filter(User.id == user_id).first()
    if db_user:
        if add_points > 0:
            db_user.points += add_points
        if add_special > 0:
            db_user.special_points += add_special
        db_user.update_time = datetime.now()
        db.commit()
        db.refresh(db_user)
    return db_user

def update_user(db: Session, user_id: int, user_update: dict):
    """更新用户信息"""
    db_user = db.query(User).filter(User.id == user_id).first()
    if db_user:
        for key, value in user_update.items():
            if hasattr(db_user, key):
                setattr(db_user, key, value)
        db_user.update_time = datetime.now()
        db.commit()
        db.refresh(db_user)
    return db_user
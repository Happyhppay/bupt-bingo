from sqlalchemy.orm import Session

from models.user_scan import UserScan


def record_user_scan(db: Session, user_id: int, club_id: int):
    """记录用户扫描社团二维码的行为"""
    user_scan = UserScan(user_id=user_id, club_id=club_id)
    db.add(user_scan)
    db.commit()
    db.refresh(user_scan)
    return user_scan

def get_by_user_id_and_club_id(db: Session, user_id: int, club_id: int):
    return db.query(UserScan).filter(UserScan.user_id == user_id, UserScan.club_id == club_id).first()
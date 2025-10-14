from sqlalchemy.orm import Session

from models.user_scan import UserScan


def get_by_user_id_and_club_id(db: Session, user_id: int, club_id: int):
    return db.query(UserScan).filter(UserScan.user_id == user_id, UserScan.club_id == club_id).first()
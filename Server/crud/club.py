from sqlalchemy.orm import Session
from models.club import Club
from schemas.club import ClubCreate, ClubUpdate

def get_club(db: Session, club_id: int):
    return db.query(Club).filter(Club.id == club_id).first()

def get_club_by_name(db: Session, club_name: str):
    return db.query(Club).filter(Club.club_name == club_name).first()

def get_clubs(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Club).offset(skip).limit(limit).all()

def create_club(db: Session, club: ClubCreate):
    db_club = Club(
        club_name=club.club_name,
        club_type=club.club_type
    )
    db.add(db_club)
    db.commit()
    db.refresh(db_club)
    return db_club

def update_club(db: Session, club_id: int, club_update: ClubUpdate):
    db_club = db.query(Club).filter(Club.id == club_id).first()
    if db_club:
        update_data = club_update.dict(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_club, key, value)
        db.commit()
        db.refresh(db_club)
    return db_club

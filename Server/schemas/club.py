from pydantic import BaseModel
from typing import Optional


class ClubBase(BaseModel):
    club_name: str
    club_type: Optional[int] = 0


class ClubUpdate(BaseModel):
    club_name: Optional[str] = None
    club_type: Optional[int] = None


class Club(ClubBase):
    id: int

    class Config:
        orm_mode = True


class QrcodeRefreshResponse(BaseModel):
    code: int
    message: str
    data: dict


class ScanQrcodeRequest(BaseModel):
    qrcodeToken: str


class ScanQrcodeResponse(BaseModel):
    code: int
    message: str
    data: dict

from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class UserBase(BaseModel):
    student_id: int
    name: str


class UserCreate(UserBase):
    pass


class UserUpdate(BaseModel):
    name: Optional[str] = None
    points: Optional[int] = None
    special_points: Optional[int] = None
    role: Optional[int] = None
    club_id: Optional[int] = None


class User(UserBase):
    id: int
    points: int
    special_points: int
    role: int
    club_id: Optional[int]
    first_entry_time: datetime
    update_time: datetime

    class Config:
        orm_mode = True


class UserLoginRequest(BaseModel):
    student_id: int
    name: str


class UserLoginResponse(BaseModel):
    code: int
    message: str
    data: dict


class InviteCodeVerifyRequest(BaseModel):
    inviteCode: str


class UserVerifyInviteResponse(BaseModel):
    code: int
    message: str
    data: dict

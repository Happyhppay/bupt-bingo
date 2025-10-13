from pydantic import BaseModel
from typing import Optional


class InviteCodeBase(BaseModel):
    code: str
    role: int
    club_id: Optional[int] = None


class InviteCodeCreate(InviteCodeBase):
    pass


class InviteCodeUpdate(BaseModel):
    is_used: Optional[int] = None
    use_time: Optional[str] = None


class InviteCode(InviteCodeBase):
    id: int
    is_used: int
    create_time: str
    use_time: Optional[str]

    class Config:
        orm_mode = True

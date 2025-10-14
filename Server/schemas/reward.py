from pydantic import BaseModel
from typing import Optional


class AwardTokenBase(BaseModel):
    user_id: int
    bingo: int
    reward_level: Optional[int] = None


class AwardTokenCreate(AwardTokenBase):
    token: str


class AwardToken(AwardTokenBase):
    id: int
    token: str
    is_verified: int
    create_time: str
    verify_time: Optional[str]

    class Config:
        orm_mode = True


class GenerateRewardQrcodeRequest(BaseModel):
    rewardLevel: int


class GenerateRewardQrcodeResponse(BaseModel):
    code: int
    message: str
    data: dict


class VerifyRewardRequest(BaseModel):
    rewardToken: str


class VerifyRewardResponse(BaseModel):
    code: int
    message: str
    data: dict

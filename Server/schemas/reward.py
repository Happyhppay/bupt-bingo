from pydantic import BaseModel


# class AwardTokenBase(BaseModel):
#     user_id: int
#     bingo: int
#     reward_level: Optional[int] = None


# class AwardTokenCreate(AwardTokenBase):
#     token: str


# class AwardToken(AwardTokenBase):
#     id: int
#     token: str
#     is_verified: int
#     create_time: str
#     verify_time: Optional[str]

#     class Config:
#         orm_mode = True


class GenerateRewardQrcodeRequest(BaseModel):
    reward: int

class GenerateRewardQrcodeData(BaseModel):
    rewardToken: str

class GenerateRewardQrcodeResponse(BaseModel):
    code: int
    message: str
    data: GenerateRewardQrcodeData


class VerifyRewardRequest(BaseModel):
    rewardToken: str

class VerifyRewardData(BaseModel):
    studentId: int
    reward: int

class VerifyRewardResponse(BaseModel):
    code: int
    message: str
    data: VerifyRewardData

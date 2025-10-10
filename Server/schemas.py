# schemas.py
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

# 用户
class UserLogin(BaseModel):
    wechatCode: str

class UserInfo(BaseModel):
    userId: str
    nickname: str
    avatar: str
    firstEnterTime: datetime
    role: str

class UserTokenResponse(BaseModel):
    userToken: str
    userInfo: UserInfo

# 邀请码
class InviteCodeVerify(BaseModel):
    inviteCode: str

class RoleResponse(BaseModel):
    role: str
    clubName: str
    newToken: str

# 二维码
class QrcodeTokenResponse(BaseModel):
    qrcodeToken: str

class ScanResponse(BaseModel):
    addedPoint: int
    addedSpecialPoint: int
    isDuplicate: bool

# Bingo
class GridStatusResponse(BaseModel):
    point: int
    specialPoint: int
    bingoGrid: List[List[int]]
    availableRewards: List[str]

class LightRequest(BaseModel):
    pointType: str
    targetGrid: Optional[str]  # "[row,col]"

class LightResponse(BaseModel):
    updatedGrid: List[List[int]]
    remainingPoint: int
    remainingSpecialPoint: int

# 领奖
class GenerateRewardRequest(BaseModel):
    bingoType: str

class RewardTokenResponse(BaseModel):
    rewardToken: str

class VerifyRewardResponse(BaseModel):
    userInfo: UserInfo
    rewardType: str
from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session
from crud.user import get_user_by_student_id
from database import get_db
from schemas.reward import GenerateRewardQrcodeRequest, GenerateRewardQrcodeResponse, VerifyRewardRequest, \
    VerifyRewardResponse
from crud.award_token import get_award_token, get_award_tokens_by_user, verify_award_token
from utils import limiter
from dependencies import get_current_user_id, get_current_admin

router = APIRouter(
    prefix="/reward",
    tags=["reward"]
)


@router.post("/qrcode", response_model=GenerateRewardQrcodeResponse)
@limiter.limit("10/minute")
def generate_reward_qrcode(
        request: Request, 
        reward_qrcode: GenerateRewardQrcodeRequest,
        db: Session = Depends(get_db),
        user_id=Depends(get_current_user_id)
):
    """生成领奖二维码"""
    reward = reward_qrcode.reward
    if reward < 1 or reward > 7:
        raise HTTPException(status_code=400, detail="Invalid reward level")

    award_tokens = get_award_tokens_by_user(db, user_id)
    reward_token = None
    for token in award_tokens:
        if token.reward == reward and token.is_verified == 0:
            reward_token = token.token
            break
    if not reward_token:
        raise HTTPException(status_code=404, detail="No unverified reward token found")

    return {
        "code": 200,
        "message": "Success",
        "data": {
            "rewardToken": reward_token
        }
    }


@router.post("/verify", response_model=VerifyRewardResponse)
@limiter.limit("1/second")
def verify_reward_qrcode(
        request: Request,
        verify_request: VerifyRewardRequest,
        db: Session = Depends(get_db),
        user_id=Depends(get_current_admin)
):
    """管理员验证领奖二维码"""
    reward_token = verify_request.rewardToken

    # 查找领奖记录
    award = get_award_token(db, reward_token)
    if not award:
        raise HTTPException(status_code=400, detail="Invalid reward token")

    # 检查是否已验证
    if award.is_verified == 1:
        raise HTTPException(status_code=400, detail="This reward token has already been verified")

    # 获取用户信息
    user = get_user_by_student_id(db, award.user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # 标记为已验证
    verify_award_token(db, award.id)

    return {
        "code": 200,
        "message": "Success",
        "data": {
            "studentId": award.user_id,
            "reward": award.reward
        }
    }

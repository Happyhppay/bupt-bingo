from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from schemas.reward import GenerateRewardQrcodeRequest, GenerateRewardQrcodeResponse, VerifyRewardRequest, \
    VerifyRewardResponse
from crud.award_token import create_award_token, get_award_token, verify_award_token
from crud.user import get_user
from crud.bingo_grid import get_user_bingo_status
from utils import generate_award_token, check_bingo_conditions
from dependencies import get_current_user, get_current_admin

router = APIRouter(
    prefix="/reward",
    tags=["reward"]
)


@router.post("/qrcode", response_model=GenerateRewardQrcodeResponse)
def generate_reward_qrcode(
        reward_request: GenerateRewardQrcodeRequest,
        db: Session = Depends(get_db),
        current_user=Depends(get_current_user)
):
    """生成领奖二维码"""
    bingo_type = reward_request.bingoType

    # 检查用户是否满足该Bingo条件
    grid_status = get_user_bingo_status(db, user_id=current_user.id)
    valid_bingos = check_bingo_conditions(grid_status)

    if bingo_type not in valid_bingos:
        raise HTTPException(status_code=400, detail=f"User does not meet {bingo_type} bingo condition")

    # 生成领奖token
    token = generate_award_token(user_id=current_user.id, bingo_type=bingo_type)

    # 创建领奖记录
    create_award_token(db, award_token={
        "token": token,
        "user_id": current_user.id,
        "bingo_type": bingo_type
    })

    return {
        "code": 200,
        "message": "Success",
        "data": {
            "rewardToken": token
        }
    }


@router.post("/verify", response_model=VerifyRewardResponse)
def verify_reward_qrcode(
        verify_request: VerifyRewardRequest,
        db: Session = Depends(get_db),
        current_admin=Depends(get_current_admin)
):
    """管理员验证领奖二维码"""
    reward_token = verify_request.rewardToken

    # 查找领奖记录
    award = get_award_token(db, token=reward_token)
    if not award:
        raise HTTPException(status_code=400, detail="Invalid reward token")

    # 检查是否已验证
    if award.is_verified == 1:
        raise HTTPException(status_code=400, detail="This reward token has already been verified")

    # 获取用户信息
    user = get_user(db, user_id=award.user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # 标记为已验证
    verify_award_token(db, token_id=award.id)

    return {
        "code": 200,
        "message": "Success",
        "data": {
            "userInfo": {
                "studentId": user.id,
                "name": user.name
            },
            "bingoType": award.bingo_type
        }
    }

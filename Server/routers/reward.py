# routers/reward.py
from fastapi import APIRouter, Depends
from schemas import RewardTokenResponse, VerifyRewardResponse
from utils import generate_hash_token
from database import SessionLocal
from models import User, RewardToken, BingoGrid
import json

router = APIRouter(prefix="/reward", tags=["奖励"])

@router.post("/qrcode", response_model=RewardTokenResponse)
def generate_reward(body: dict, current_user=Depends(get_current_user)):
    bingo_type = body.get("bingoType")
    db = SessionLocal()

    user = db.query(User).filter(User.user_id == current_user["sub"]).first()
    if not user:
        raise HTTPException(status_code=404, detail="用户不存在")

    # 验证是否达成该 Bingo
    grid_record = db.query(BingoGrid).filter(BingoGrid.user_id == user.id).first()
    grid = json.loads(grid_record.grid_data)
    available = [r for r in ["横向1", "横向2", "横向3", "横向4", "横向5",
                             "竖向1", "竖向2", "竖向3", "竖向4", "竖向5",
                             "斜向1", "斜向2", "全收集"] if r in check_bingo(grid)]
    if bingo_type not in available:
        raise HTTPException(status_code=400, detail="未达成该 Bingo")

    token_str = generate_hash_token("reward", f"{user.user_id}_{bingo_type}")
    reward_token = RewardToken(
        token=token_str,
        user_id=user.id,
        bingo_type=bingo_type,
        claimed=False
    )
    db.add(reward_token)
    db.commit()

    db.close()
    return {
        "code": 200,
        "msg": "领奖二维码生成成功",
        "data": {"rewardToken": token_str}
    }

@router.post("/verify", dependencies=[Depends(require_role("admin"))])
def verify_reward(body: dict):
    token = body.get("rewardToken")
    db = SessionLocal()

    record = db.query(RewardToken).filter(RewardToken.token == token).first()
    if not record:
        raise HTTPException(status_code=404, detail="领奖码不存在")
    if record.claimed:
        raise HTTPException(status_code=400, detail="已领取")

    user = db.query(User).filter(User.id == record.user_id).first()
    record.claimed = True
    record.claimed_at = datetime.utcnow()
    db.commit()

    db.close()
    return {
        "code": 200,
        "msg": "验证成功",
        "data": {
            "userInfo": {
                "userId": user.user_id,
                "nickname": user.nickname,
                "avatar": user.avatar
            },
            "rewardType": record.bingo_type
        }
    }
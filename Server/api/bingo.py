from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session
import random
from crud.award_token import create_award_token, get_award_token, get_award_tokens_by_user
from database import get_db
from schemas.bingo import BingoStatusResponse, LightBingoRequest, LightBingoResponse
from crud.bingo_grid import get_user_bingo_status, set_bingo_grid_lit
from crud.user import get_user_by_student_id, update_user
from dependencies import get_current_user_id
from utils import generate_award_token, get_bingo_nums, limiter

router = APIRouter(
    prefix="/bingo",
    tags=["bingo"]
)


@router.get("/status", response_model=BingoStatusResponse)
@limiter.limit("10/minute")
def get_bingo_status(
        request: Request, 
        db: Session = Depends(get_db),
        user_id=Depends(get_current_user_id)
):
    """获取当前Bingo状态"""
    user = get_user_by_student_id(db, user_id)
    # 获取用户的Bingo格子状态
    grid_status = get_user_bingo_status(db, user_id)

    rewards = list()
    award_tokens = get_award_tokens_by_user(db, user_id)
    for token in award_tokens:
        rewards.append(token.reward)

    return {
        "code": 200,
        "message": "Success",
        "data": {
            "point": user.points,
            "specialPoint": user.special_points,
            "bingoGrid": grid_status,
            "rewards": rewards
        }
    }


@router.post("/light", response_model=LightBingoResponse)
@limiter.limit("1/second")
def light_bingo_grid(
        request: Request, 
        light_request: LightBingoRequest,
        db: Session = Depends(get_db),
        user_id=Depends(get_current_user_id)
):
    """点亮Bingo格子"""
    point_type = light_request.pointType
    location = light_request.location

    user = get_user_by_student_id(db, user_id)

    # 检查积分是否足够
    if point_type == "normal":
        if user.points < 1:
            raise HTTPException(status_code=400, detail="Not enough normal points")
    elif point_type == "special":
        if user.special_points < 1:
            raise HTTPException(status_code=400, detail="Not enough special points")
        if not location or len(location) != 2:
            raise HTTPException(status_code=400, detail="Location is required for special points")
    else:
        raise HTTPException(status_code=400, detail="Invalid point type")

    # 确定要点亮的格子位置
    row, col = 0, 0
    if point_type == "normal":
        # 普通积分：随机点亮一个未点亮的格子
        grid_status = get_user_bingo_status(db, user_id)
        unlit_cells = []

        for i in range(5):
            for j in range(5):
                if grid_status[i][j] == 0:
                    unlit_cells.append((i, j))

        if not unlit_cells:
            raise HTTPException(status_code=400, detail="All cells are already lit")

        # 随机选择一个未点亮的格子
        row, col = random.choice(unlit_cells)
    else:  # special
        # 特殊积分：使用指定位置
        row = location[0]
        col = location[1]
        if row < 0 or row > 4 or col < 0 or col > 4:
            raise HTTPException(status_code=400, detail="Invalid location")

    # 点亮格子
    set_bingo_grid_lit(db, user_id, row, col, 1)
    grid_status = get_user_bingo_status(db, user_id)
    bingo = get_bingo_nums(grid_status)
    if bingo > user.bingo:
        update_user(db, user_id, {"bingo": bingo})

        rewards_now = list()
        award_tokens = get_award_tokens_by_user(db, user_id)
        for token in award_tokens:
            rewards_now.append(token.reward)
        if len(rewards_now) < 6:
            not_get_rewards = [i for i in range(1, 7) if i not in rewards_now]
            reward = random.choice(not_get_rewards)
            token = generate_award_token(user_id, f"{reward}")
            create_award_token(db, token, user_id, reward)

    # 扣除相应积分
    if point_type == "normal":
        update_user(db, user_id=user_id, user_update={"points": user.points - 1})
    else:
        update_user(db, user_id=user_id, user_update={"special_points": user.special_points - 1})

    # 获取更新后的状态
    updated_user = get_user_by_student_id(db, user_id)
    updated_grid_status = get_user_bingo_status(db, user_id)
    updated_rewards = list()
    award_tokens = get_award_tokens_by_user(db, user_id)
    for token in award_tokens:
        updated_rewards.append(token.reward)

    return {
        "code": 200,
        "message": "Success",
        "data": {
            "point": updated_user.points,
            "specialPoint": updated_user.special_points,
            "bingoGrid": updated_grid_status,
            "rewards": updated_rewards
        }
    }

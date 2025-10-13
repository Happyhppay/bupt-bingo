from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
import random
from database import get_db
from schemas.bingo import BingoStatusResponse, LightBingoRequest, LightBingoResponse
from crud.bingo_grid import get_user_bingo_status, set_bingo_grid_lit
from crud.user import get_user, update_user
from dependencies import get_current_user
from utils import check_bingo_conditions

router = APIRouter(
    prefix="/bingo",
    tags=["bingo"]
)


@router.get("/status", response_model=BingoStatusResponse)
def get_bingo_status(
        db: Session = Depends(get_db),
        current_user=Depends(get_current_user)
):
    """获取当前Bingo状态"""
    # 获取用户的Bingo格子状态
    grid_status = get_user_bingo_status(db, user_id=current_user.id)

    # 检查Bingo条件
    bingo_types = check_bingo_conditions(grid_status)

    return {
        "code": 200,
        "message": "Success",
        "data": {
            "point": current_user.points,
            "specialPoint": current_user.special_points,
            "bingoGrid": grid_status,
            "bingoType": bingo_types
        }
    }


@router.post("/light", response_model=LightBingoResponse)
def light_bingo_grid(
        light_request: LightBingoRequest,
        db: Session = Depends(get_db),
        current_user=Depends(get_current_user)
):
    """点亮Bingo格子"""
    point_type = light_request.pointType
    location = light_request.location

    # 检查积分是否足够
    if point_type == "normal":
        if current_user.points < 1:
            raise HTTPException(status_code=400, detail="Not enough normal points")
    elif point_type == "special":
        if current_user.special_points < 1:
            raise HTTPException(status_code=400, detail="Not enough special points")
        if not location or len(location) != 2:
            raise HTTPException(status_code=400, detail="Location is required for special points")
    else:
        raise HTTPException(status_code=400, detail="Invalid point type")

    # 确定要点亮的格子位置
    row, col = 0, 0
    if point_type == "normal":
        # 普通积分：随机点亮一个未点亮的格子
        grid_status = get_user_bingo_status(db, user_id=current_user.id)
        unlit_cells = []

        for i in range(5):
            for j in range(5):
                if grid_status[i][j] == 0:
                    unlit_cells.append((i + 1, j + 1))  # 转换为1-based

        if not unlit_cells:
            raise HTTPException(status_code=400, detail="All cells are already lit")

        # 随机选择一个未点亮的格子
        row, col = random.choice(unlit_cells)
    else:  # special
        # 特殊积分：使用指定位置（转换为1-based）
        row = location[0] + 1
        col = location[1] + 1

        # 验证位置有效性
        if row < 1 or row > 5 or col < 1 or col > 5:
            raise HTTPException(status_code=400, detail="Invalid location")

    # 点亮格子
    set_bingo_grid_lit(db, user_id=current_user.id, row=row, col=col, is_lit=1)

    # 扣除相应积分
    if point_type == "normal":
        update_user(db, user_id=current_user.id, user_update={"points": current_user.points - 1})
    else:
        update_user(db, user_id=current_user.id, user_update={"special_points": current_user.special_points - 1})

    # 获取更新后的状态
    updated_user = get_user(db, user_id=current_user.id)
    updated_grid_status = get_user_bingo_status(db, user_id=current_user.id)
    bingo_types = check_bingo_conditions(updated_grid_status)

    return {
        "code": 200,
        "message": "Success",
        "data": {
            "point": updated_user.points,
            "specialPoint": updated_user.special_points,
            "bingoGrid": updated_grid_status,
            "bingoType": bingo_types
        }
    }

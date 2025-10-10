# routers/bingo.py
from fastapi import APIRouter, Depends
from schemas import GridStatusResponse, LightResponse
from utils import check_bingo, init_bingo_grid
from database import SessionLocal
from models import User, BingoGrid
import json

router = APIRouter(prefix="/bingo", tags=["Bingo"])

@router.get("/status", response_model=GridStatusResponse)
def get_status(current_user=Depends(get_current_user)):
    db = SessionLocal()
    user = db.query(User).filter(User.user_id == current_user["sub"]).first()
    if not user:
        raise HTTPException(status_code=404, detail="用户不存在")

    grid_record = db.query(BingoGrid).filter(BingoGrid.user_id == user.id).first()
    if not grid_record:
        grid_data = init_bingo_grid()
        grid_record = BingoGrid(user_id=user.id, grid_data=json.dumps(grid_data))
        db.add(grid_record)
        db.commit()
    else:
        grid_data = json.loads(grid_record.grid_data)

    rewards = check_bingo(grid_data)

    db.close()
    return {
        "code": 200,
        "msg": "查询成功",
        "data": {
            "point": user.point,
            "specialPoint": user.special_point,
            "bingoGrid": grid_data,
            "availableRewards": rewards
        }
    }

@router.post("/light", response_model=LightResponse)
def light_cell(body: dict, current_user=Depends(get_current_user)):
    point_type = body.get("pointType")
    target = body.get("targetGrid")  # "[1,2]"
    db = SessionLocal()

    user = db.query(User).filter(User.user_id == current_user["sub"]).first()
    if not user:
        raise HTTPException(status_code=404, detail="用户不存在")

    grid_record = db.query(BingoGrid).filter(BingoGrid.user_id == user.id).first()
    grid = json.loads(grid_record.grid_data)

    if point_type == "normal":
        if user.point <= 0:
            raise HTTPException(status_code=400, detail="积分不足")
        # 自动点亮第一个未点亮格子（简化）
        for i in range(5):
            for j in range(5):
                if grid[i][j] == 0:
                    grid[i][j] = 1
                    user.point -= 1
                    break
            else:
                continue
            break
    elif point_type == "special":
        if user.special_point <= 0:
            raise HTTPException(status_code=400, detail="特殊积分不足")
        if not target:
            raise HTTPException(status_code=400, detail="需指定目标格子")
        try:
            r, c = map(int, target.strip('[]').split(','))
            if grid[r][c] == 1:
                raise HTTPException(status_code=400, detail="格子已点亮")
            grid[r][c] = 1
            user.special_point -= 1
        except Exception:
            raise HTTPException(status_code=400, detail="格子坐标无效")
    else:
        raise HTTPException(status_code=400, detail="积分类型错误")

    grid_record.grid_data = json.dumps(grid)
    db.commit()
    db.refresh(user)

    db.close()
    return {
        "code": 200,
        "msg": "格子点亮成功",
        "data": {
            "updatedGrid": grid,
            "remainingPoint": user.point,
            "remainingSpecialPoint": user.special_point
        }
    }
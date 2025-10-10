# routers/auth.py
from fastapi import APIRouter, Depends
from schemas import UserTokenResponse, RoleResponse
from utils import create_jwt_token, generate_invite_code
from database import SessionLocal
from models import User, InviteCode
import random

router = APIRouter(prefix="/users", tags=["用户"])

# 模拟微信登录（实际应调用微信 API）
@router.post("/login", response_model=UserTokenResponse)
def login(body: dict):
    wechatCode = body.get("wechatCode")
    if not wechatCode:
        raise HTTPException(status_code=400, detail="缺少 wechatCode")

    db = SessionLocal()
    # 模拟用户信息
    open_id = f"u{random.randint(100000, 999999)}"
    user = db.query(User).filter(User.user_id == open_id).first()
    if not user:
        user = User(
            user_id=open_id,
            nickname="玩家" + open_id[-4:],
            avatar="https://example.com/avatar.jpg",
            role="normal"
        )
        db.add(user)
        db.commit()
        db.refresh(user)

    token_data = {
        "sub": open_id,
        "role": user.role,
        "userId": user.user_id
    }
    token = create_jwt_token(token_data)
    db.close()

    return {
        "code": 200,
        "msg": "登录成功",
        "data": {
            "userToken": token,
            "userInfo": {
                "userId": user.user_id,
                "nickname": user.nickname,
                "avatar": user.avatar,
                "firstEnterTime": user.first_enter_time,
                "role": user.role
            }
        }
    }

@router.post("/verify", response_model=RoleResponse)
def verify_invite(body: dict):
    invite_code = body.get("inviteCode")
    db = SessionLocal()
    record = db.query(InviteCode).filter(InviteCode.code == invite_code).first()
    if not record:
        raise HTTPException(status_code=400, detail="邀请码无效")

    # 生成新 token 并更新用户角色（此处简化）
    new_token = create_jwt_token({
        "sub": "admin",
        "role": record.role,
        "club": record.club_name or "admin"
    })

    db.close()
    return {
        "code": 200,
        "msg": "邀请码验证成功",
        "data": {
            "role": record.role,
            "clubName": record.club_name or "admin",
            "newToken": new_token
        }
    }
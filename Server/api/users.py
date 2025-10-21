from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session
from datetime import timedelta

from database import get_db
from schemas.user import UserLoginRequest, UserLoginResponse, VerifyInviteCodeResponse, VerifyInviteCodeRequest
from crud.user import get_user_by_student_id, create_user, update_user_role
from crud.invite_code import get_valid_unused_invite_code, update_invite_code_status
from crud.club import get_club_by_id
from utils import create_access_token, limiter
from dependencies import get_current_user_id

router = APIRouter(
    prefix="/users",
    tags=["users"]
)


@router.post("/login", response_model=UserLoginResponse)
# @limiter.limit("5/minute")
def student_login(request: Request, login: UserLoginRequest, db: Session = Depends(get_db)):
    """学号姓名登录接口"""
    student_id = login.student_id
    # 查找用户
    user = get_user_by_student_id(db, student_id)

    if not user:
        # 自动注册新用户
        try:
            user = create_user(db, student_id)
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"用户注册失败: {str(e)}")

    # 生成JWT令牌
    access_token_expires = timedelta(days=10)
    access_token = create_access_token(
        data={
            "sub": user.id,
            "role": 0
            },
        expires_delta=access_token_expires
    )

    return {
        "code": 200,
        "message": "登录成功",
        "data": {
            "userToken": access_token,
            "userInfo": {
                "studentId": user.id,
                "firstEnterTime": user.first_entry_time.isoformat(),
                "role": "normal"
            }
        }
    }


@router.post("/verify", response_model=VerifyInviteCodeResponse)
@limiter.limit("5/hour")
def verify_invite_code(request: Request, invite: VerifyInviteCodeRequest, db: Session = Depends(get_db), user_id=Depends(get_current_user_id)):
    """验证邀请码，获取管理员/社团成员权限

    接收 JSON body: { "inviteCode": "..." }
    """
    # 从请求体中读取邀请码
    inviteCode = invite.inviteCode
    # 查找有效的未使用邀请码
    code = get_valid_unused_invite_code(db, inviteCode)
    if not code:
        raise HTTPException(status_code=400, detail="邀请码无效或已被使用")
    role = code.role
    club_id = code.club_id if code.club_id else None

    # 更新用户角色
    updated_user = update_user_role(
        db=db,
        user_id=user_id,
        role=role,
        club_id=club_id
    )

    # 标记邀请码为已使用
    update_invite_code_status(db, code_id=code.id)

    # 生成新的令牌
    access_token_expires = timedelta(days=10)
    new_token = create_access_token(
        data={
            "sub": user_id,
            "role": int(code.role)
            },
        expires_delta=access_token_expires
    )

    # 准备返回信息
    role_str = "club" if int(code.role) == 1 else "admin"
    club_name = "admin"

    if int(code.role) == 1 and code.club_id is not None:
        club = get_club_by_id(db, club_id=int(code.club_id))
        club_name = club.club_name if club else "未知社团"

    return {
        "code": 200,
        "message": "邀请码验证成功",
        "data": {
            "role": role_str,
            "clubName": club_name,
            "newToken": new_token
        }
    }

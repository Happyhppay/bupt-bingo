from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import timedelta

from database import get_db
from schemas.user import UserLoginRequest, UserLoginResponse, UserVerifyInviteResponse, InviteCodeVerifyRequest
from crud.user import get_user_by_student_id_and_name, create_user, update_user_role
from crud.invite_code import get_valid_unused_invite_code, update_invite_code_status
from crud.club import get_club
from utils import create_access_token, role_to_str
from dependencies import get_current_user

router = APIRouter(
    prefix="/users",
    tags=["users"]
)


@router.post("/login", response_model=UserLoginResponse)
def student_login(login_data: UserLoginRequest, db: Session = Depends(get_db)):
    """学号姓名登录接口"""
    # 查找用户
    user = get_user_by_student_id_and_name(db, student_id=login_data.student_id, name=login_data.name)

    if not user:
        # 自动注册新用户
        try:
            user = create_user(
                db=db,
                student_id=login_data.student_id,
                name=login_data.name
            )
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"用户注册失败: {str(e)}")

    # 生成JWT令牌
    access_token_expires = timedelta(days=10)
    access_token = create_access_token(
        data={"sub": user.id}, expires_delta=access_token_expires
    )

    # 转换角色为字符串
    role_str = role_to_str(user.role)

    return {
        "code": 200,
        "message": "登录成功",
        "data": {
            "userToken": access_token,
            "userInfo": {
                "studentId": user.id,
                "name": user.name,
                "firstEnterTime": user.first_entry_time.isoformat(),
                "role": role_str
            }
        }
    }


@router.post("/verify", response_model=UserVerifyInviteResponse)
def verify_invite_code(invite: InviteCodeVerifyRequest, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    """验证邀请码，获取管理员/社团成员权限

    接收 JSON body: { "inviteCode": "..." }
    """
    # 从请求体中读取邀请码
    inviteCode = invite.inviteCode
    # 查找有效的未使用邀请码
    code = get_valid_unused_invite_code(db, code=inviteCode)
    if not code:
        raise HTTPException(status_code=400, detail="邀请码无效或已被使用")

    # 更新用户角色
    updated_user = update_user_role(
        db=db,
        user_id=current_user.id,
        role=int(code.role),
        club_id=int(code.club_id) if code.club_id else None
    )

    # 标记邀请码为已使用
    update_invite_code_status(db, code_id=int(code.id))

    # 生成新的令牌
    access_token_expires = timedelta(days=10)
    new_token = create_access_token(
        data={"sub": updated_user.id}, expires_delta=access_token_expires
    )

    # 准备返回信息
    role_str = "club" if int(code.role) == 1 else "admin"
    club_name = "admin"

    if int(code.role) == 1 and code.club_id is not None:
        club = get_club(db, club_id=int(code.club_id))
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

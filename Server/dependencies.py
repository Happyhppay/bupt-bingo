from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from utils import decode_access_token

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def get_current_user_id(token: str = Depends(oauth2_scheme)):
    """获取当前登录用户"""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    payload = decode_access_token(token)
    if payload is None:
        raise credentials_exception

    user_id: int = payload.get("sub")
    if user_id is None:
        raise credentials_exception

    return user_id

def get_current_role(token: str = Depends(oauth2_scheme)):
    """获取当前登录用户角色"""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    payload = decode_access_token(token)
    if payload is None:
        raise credentials_exception

    role: int = payload.get("role")
    if role is None:
        raise credentials_exception
    return role


def get_current_club_member(user_id=Depends(get_current_user_id), role=Depends(get_current_role)):
    """获取当前社团成员用户"""
    if role != 1:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions (requires club member)"
        )
    return user_id


def get_current_admin(user_id=Depends(get_current_user_id), role=Depends(get_current_role)):
    """获取当前管理员用户"""
    if role != 2:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions (requires admin)"
        )
    return user_id

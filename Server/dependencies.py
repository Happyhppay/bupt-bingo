# dependencies.py
from fastapi import Depends, Header, HTTPException
from utils import decode_jwt_token

def get_current_user(authorization: str = Header(...)):
    if not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="未提供 Token")
    token = authorization.split(" ")[1]
    payload = decode_jwt_token(token)
    return payload

def require_role(required_role: str):
    def _check(user = Depends(get_current_user)):
        if user.get("role") != required_role:
            raise HTTPException(status_code=403, detail="权限不足")
        return user
    return _check
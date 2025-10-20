from fastapi import Request
import jwt
import hashlib
import random
import string
from datetime import datetime, timedelta
import os
from dotenv import load_dotenv

from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address

load_dotenv()

# JWT配置
SECRET_KEY = os.getenv("SECRET_KEY", "your-secret-key")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 10 * 24 * 60  # 10天


def create_access_token(data: dict, expires_delta: timedelta = None):
    """创建JWT令牌"""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def decode_access_token(token: str):
    """解码JWT令牌"""
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except jwt.PyJWTError:
        return None


def generate_random_string(length: int = 16):
    """生成随机字符串"""
    letters = string.ascii_letters + string.digits
    return ''.join(random.choice(letters) for _ in range(length))


def generate_token(data: str):
    """生成基于数据的哈希令牌"""
    # 添加随机盐值增加安全性
    salt = generate_random_string(8)
    hash_object = hashlib.sha256(f"{data}{salt}".encode())
    return hash_object.hexdigest()


def generate_club_qrcode_token(club_id: int):
    """生成社团二维码token"""
    random_str = generate_random_string(16)
    return generate_token(f"club_{club_id}_{random_str}")


def generate_award_token(user_id: int, reward_level: str):
    """生成领奖token"""
    timestamp = datetime.now().timestamp()
    return generate_token(f"user_{user_id}_{reward_level}_{timestamp}")


def get_bingo_nums(grid_status) -> int:
    """
    检查Bingo条件
    grid_status: 5x5矩阵，1表示点亮，0表示未点亮
    返回满足条件的Bingo类型列表
    """
    bingo_nums: int = 0

    # 检查横向
    for i in range(5):
        if all(grid_status[i][j] == 1 for j in range(5)):
            bingo_nums += 1

    # 检查竖向
    for j in range(5):
        if all(grid_status[i][j] == 1 for i in range(5)):
            bingo_nums += 1

    # 检查斜向1（左上到右下）
    if all(grid_status[i][i] == 1 for i in range(5)):
        bingo_nums += 1

    # 检查斜向2（右上到左下）
    if all(grid_status[i][4 - i] == 1 for i in range(5)):
        bingo_nums += 1

    return bingo_nums


def role_to_str(role: int) -> str:
    """Convert numeric role to string representation."""
    try:
        r = int(role)
    except Exception:
        return "normal"

    if r == 1:
        return "club"
    if r == 2:
        return "admin"
    return "normal"

def token_key_func(request: Request) -> str:
    """用于限流的token键函数"""
    token = request.headers.get("Authorization")
    if token:
        payload = decode_access_token(token)
        if payload:
            user_id: int = payload.get("sub")
            return user_id
    return get_remote_address(request)

limiter = Limiter(key_func=token_key_func)
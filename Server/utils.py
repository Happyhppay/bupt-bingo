# utils.py
import jwt
import hashlib
import random
import string
from datetime import datetime, timedelta
from fastapi import HTTPException
from config import SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE_DAYS

def create_jwt_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(days=ACCESS_TOKEN_EXPIRE_DAYS))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def decode_jwt_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token 已过期")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="无效 Token")

def generate_hash_token(prefix: str, salt: str = "") -> str:
    raw = prefix + salt + ''.join(random.choices(string.ascii_letters + string.digits, k=8))
    return hashlib.sha256(raw.encode()).hexdigest()[:32]

def generate_invite_code(role: str, club_name: str = ""):
    return f"{role}_{club_name}_{random.randint(1000, 9999)}"

# 初始 Bingo 网格
def init_bingo_grid():
    return [[0]*5 for _ in range(5)]

# 检查 Bingo 类型
def check_bingo(grid):
    rewards = []
    n = 5

    # 横向
    for i in range(n):
        if all(grid[i][j] == 1 for j in range(n)):
            rewards.append(f"横向{i+1}")

    # 竖向
    for j in range(n):
        if all(grid[i][j] == 1 for i in range(n)):
            rewards.append(f"竖向{j+1}")

    # 斜向
    if all(grid[i][i] == 1 for i in range(n)):
        rewards.append("斜向1")
    if all(grid[i][n-1-i] == 1 for i in range(n)):
        rewards.append("斜向2")

    # 全图
    if all(grid[i][j] == 1 for i in range(n) for j in range(n)):
        rewards.append("全收集")

    return rewards
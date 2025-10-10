# config.py
import os
from datetime import timedelta

SECRET_KEY = os.getenv("SECRET_KEY", "your-super-secret-jwt-key")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_DAYS = 7
DATABASE_URL = "sqlite:///./bingo.db"  # 可替换为 PostgreSQL
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from database import engine, Base
from api.users import router as users_router
from api.clubs import router as clubs_router
from api.bingo import router as bingo_router
from api.reward import router as reward_router
from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from slowapi.middleware import SlowAPIMiddleware
from utils import limiter

app = FastAPI(
    title="Bingo H5 小游戏 API",
    description="社团游园会 Bingo 小游戏后端 API",
    version="1.0.0"
)
# 注册路由
app.include_router(users_router)
app.include_router(clubs_router)
app.include_router(bingo_router)
app.include_router(reward_router)

app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)
app.add_middleware(SlowAPIMiddleware)

try:
    from database import Base, engine
    Base.metadata.create_all(bind=engine)
except Exception as e:
    print("应用启动时创建数据表失败: ", e)
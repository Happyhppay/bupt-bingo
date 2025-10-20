from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from database import engine, Base
from api.users import router as users_router
from api.clubs import router as clubs_router
from api.bingo import router as bingo_router
from api.reward import router as reward_router

app = FastAPI(
    title="Bingo H5 小游戏 API",
    description="社团游园会 Bingo 小游戏后端 API",
    version="1.0.0"
)

# 配置CORS
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"],
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

# 注册路由
app.include_router(users_router)
app.include_router(clubs_router)
app.include_router(bingo_router)
app.include_router(reward_router)

try:
    from database import Base, engine
    Base.metadata.create_all(bind=engine)
except Exception as e:
    print("应用启动时创建数据表失败: ", e)
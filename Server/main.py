from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from database import engine, Base
from api.users import router as users_router
from api.clubs import router as clubs_router
from api.bingo import router as bingo_router
from api.reward import router as reward_router

# 创建数据库表
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Bingo H5 小游戏 API",
    description="社团游园会 Bingo 小游戏后端 API",
    version="1.0.0"
)

# 配置CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 注册路由
app.include_router(users_router)
app.include_router(clubs_router)
app.include_router(bingo_router)
app.include_router(reward_router)

@app.get("/")
def read_root():
    return {"message": "Welcome to Bingo H5 Game API"}

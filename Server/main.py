# main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from database import Base, engine
import routers.auth, routers.clubs, routers.bingo, routers.reward

# 创建数据库表
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Bingo H5 小游戏 API", version="1.0.0")

# 允许跨域（前端 H5）
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 注册路由
app.include_router(routers.auth.router)
app.include_router(routers.clubs.router)
app.include_router(routers.bingo.router)
app.include_router(routers.reward.router)

@app.get("/")
def root():
    return {"message": "Welcome to Bingo Game API"}
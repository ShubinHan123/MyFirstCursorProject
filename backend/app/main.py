import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.routes import router as api_router
from app.core.config import settings
from app.db.init_db import init_db

# 初始化数据库
init_db()

# 创建必要的目录
os.makedirs("data", exist_ok=True)  # 数据库目录
os.makedirs(settings.UPLOAD_DIR, exist_ok=True)
os.makedirs(settings.DOCS_DIR, exist_ok=True)
os.makedirs(settings.JSON_DIR, exist_ok=True)
os.makedirs(settings.ENTS_DIR, exist_ok=True)

app = FastAPI(
    title=settings.PROJECT_NAME,
    description="用于上传、处理及分析PDF文件，并通过图形化方式展示文档与实体之间的关系",
    version=settings.VERSION
)

# 配置CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 在生产环境中应该设置具体的域名
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 包含API路由
app.include_router(api_router, prefix=settings.API_V1_STR)

@app.get("/")
async def root():
    return {"message": "欢迎使用PDF文档实体识别与关系可视化平台API"} 
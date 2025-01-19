import os
from pydantic import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str = "PDF文档实体识别与关系可视化平台"
    VERSION: str = "1.0.0"
    API_V1_STR: str = "/api/v1"
    
    # 数据库配置
    SQLALCHEMY_DATABASE_URI: str = os.getenv(
        "DATABASE_URL",
        "sqlite:///./data/app.db"
    )
    
    # 文件存储路径
    UPLOAD_DIR: str = "papers"
    DOCS_DIR: str = "docs"
    JSON_DIR: str = "json"
    ENTS_DIR: str = "ents"
    
    # SpaCy模型
    SPACY_MODEL: str = "en_core_web_sm"
    
    class Config:
        case_sensitive = True

settings = Settings() 
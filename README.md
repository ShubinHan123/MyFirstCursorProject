# PDF文档实体识别与关系可视化平台

本项目是一个基于 FastAPI 和 React 的 Web 应用，用于处理 PDF 文档，提取实体信息并可视化展示实体之间的关系。

## 功能特点

- PDF 文档上传和管理
- 自动将 PDF 转换为 DOCX 格式
- 使用 spaCy 进行实体识别
- 实体关系可视化
- 文档全文检索
- 实体统计分析

## 技术栈

### 后端
- Python 3.12
- FastAPI
- SQLAlchemy
- spaCy
- pdf2docx
- python-docx

### 前端
- React 18
- Ant Design 4
- Axios
- D3.js

## 安装说明

### 1. 环境要求
- Python 3.12 或更高版本
- Node.js 18 或更高版本
- pip 和 npm 包管理器

### 2. 后端设置
```bash
# 创建虚拟环境
python -m venv .venv

# 激活虚拟环境
# Windows:
.\.venv\Scripts\activate.bat
# Linux/Mac:
source .venv/bin/activate

# 安装依赖
cd backend
pip install -r requirements.txt

# 安装 spaCy 语言模型
python -m spacy download en_core_web_sm
```

### 3. 前端设置
```bash
cd frontend
npm install
```

## 启动项目

### 启动后端
```bash
cd backend
uvicorn app.main:app --reload --port 8000
```

### 启动前端
```bash
cd frontend
npm start
```

## 项目结构
```
├── backend/
│   ├── app/
│   │   ├── api/
│   │   ├── core/
│   │   ├── db/
│   │   ├── models/
│   │   ├── schemas/
│   │   └── services/
│   └── requirements.txt
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   ├── pages/
│   │   ├── services/
│   │   └── utils/
│   └── package.json
├── data/
├── docs/
├── papers/
├── json/
└── ents/
```

## 使用说明

1. 访问 http://localhost:3000 打开前端界面
2. 使用上传功能添加 PDF 文档
3. 系统会自动处理文档并提取实体
4. 在实体列表页面查看识别出的实体
5. 在关系图谱页面查看实体之间的关系

## API 文档

访问 http://localhost:8000/docs 查看完整的 API 文档。

## 注意事项

- 确保所有必要的目录（data, docs, papers, json, ents）都已创建
- PDF 文件大小限制为 50MB
- 建议使用 Chrome 或 Firefox 浏览器

## 开发说明

- 后端代码修改会自动重载
- 前端代码修改会自动热更新
- 数据库结构修改需要重启后端服务

## 许可证

MIT License 
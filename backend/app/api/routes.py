from fastapi import APIRouter, Depends, File, UploadFile, HTTPException
from sqlalchemy.orm import Session
from typing import List
import os

from app.db.session import get_db
from app.services.pdf_processor import process_pdf
from app.schemas.paper import Paper, PaperCreate
from app.schemas.entity import Entity, EntityCreate
from app.services import crud

router = APIRouter()

@router.post("/upload/", response_model=Paper)
async def upload_pdf(
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    """
    上传PDF文件并处理
    """
    if not file.filename.endswith('.pdf'):
        raise HTTPException(status_code=400, detail="只能上传PDF文件")
    
    try:
        # 保存文件
        file_path = os.path.join("papers", file.filename)
        with open(file_path, "wb") as buffer:
            content = await file.read()
            buffer.write(content)
        
        # 处理PDF文件
        paper_data = await process_pdf(file_path)
        
        # 创建数据库记录
        paper = crud.create_paper(db, PaperCreate(**paper_data))
        return paper
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/papers/", response_model=List[Paper])
def get_papers(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """
    获取所有论文列表
    """
    papers = crud.get_papers(db, skip=skip, limit=limit)
    return papers

@router.get("/papers/{paper_id}", response_model=Paper)
def get_paper(
    paper_id: int,
    db: Session = Depends(get_db)
):
    """
    获取单个论文详情
    """
    paper = crud.get_paper(db, paper_id=paper_id)
    if paper is None:
        raise HTTPException(status_code=404, detail="论文不存在")
    return paper

@router.get("/entities/", response_model=List[Entity])
def get_entities(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """
    获取所有实体列表
    """
    entities = crud.get_entities(db, skip=skip, limit=limit)
    return entities

@router.get("/search/")
def search_entities(
    query: str,
    entity_type: str = None,
    db: Session = Depends(get_db)
):
    """
    搜索实体
    """
    results = crud.search_entities(db, query=query, entity_type=entity_type)
    return results

@router.get("/graph/")
def get_knowledge_graph(
    db: Session = Depends(get_db)
):
    """
    获取知识图谱数据
    """
    nodes = []
    edges = []
    
    # 获取所有论文和实体
    papers = crud.get_papers(db)
    entities = crud.get_entities(db)
    
    # 构建节点
    for paper in papers:
        nodes.append({
            "id": f"p{paper.paper_id}",
            "label": paper.paper_name,
            "type": "paper"
        })
    
    for entity in entities:
        nodes.append({
            "id": f"e{entity.entity_id}",
            "label": entity.entity_name,
            "type": entity.entity_type
        })
        
        # 构建边
        for paper in entity.papers:
            edges.append({
                "source": f"p{paper.paper_id}",
                "target": f"e{entity.entity_id}",
                "value": 1  # 可以用count值
            })
    
    return {
        "nodes": nodes,
        "edges": edges
    } 
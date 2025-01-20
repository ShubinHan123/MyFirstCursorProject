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

@router.post("/papers/upload/")
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
        # 创建上传目录
        os.makedirs("papers", exist_ok=True)
        
        # 保存文件
        file_path = os.path.join("papers", file.filename)
        with open(file_path, "wb") as buffer:
            content = await file.read()
            buffer.write(content)
        
        # 处理PDF文件
        paper_data = await process_pdf(file_path, db)
        return paper_data
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/papers/")
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

@router.get("/papers/{paper_id}")
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

@router.get("/entities/")
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

@router.get("/entities/search/")
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

@router.delete("/papers/{paper_id}")
async def delete_paper_endpoint(
    paper_id: int,
    db: Session = Depends(get_db)
):
    """
    删除论文及其相关文件和关系
    """
    success = crud.delete_paper(db, paper_id)
    if success:
        # 清理没有关联的实体
        crud.cleanup_unused_entities(db)
        return {"message": "文档已删除"}
    else:
        raise HTTPException(status_code=404, detail="文档不存在或删除失败")

@router.get("/papers/search/")
def search_papers(
    query: str,
    db: Session = Depends(get_db)
):
    """
    搜索论文
    支持的查询格式：
    - get all papers that mention person [name]
    - get all papers that mention organisation [name]
    - get all papers that mention work [name]
    - get one paper that mention ...
    """
    query_parts = query.lower().split()
    if not query_parts or query_parts[0] != "get":
        raise HTTPException(status_code=400, detail="查询格式不正确")
    
    try:
        # 解析查询
        limit = None
        if query_parts[1] == "one":
            limit = 1
            query_parts.pop(1)
        
        if query_parts[1] != "all" or query_parts[2] != "papers" or \
           query_parts[3] != "that" or query_parts[4] != "mention":
            raise HTTPException(status_code=400, detail="查询格式不正确")
        
        # 获取实体类型和名称
        entity_type = None
        if query_parts[5] == "person":
            entity_type = "PERSON"
            name_start = 6
        elif query_parts[5] == "organisation":
            entity_type = "ORG"
            name_start = 6
        elif query_parts[5] == "work":
            entity_type = "WORK_OF_ART"
            name_start = 6
        else:
            name_start = 5
        
        entity_name = " ".join(query_parts[name_start:])
        
        # 执行搜索
        papers = crud.search_papers_by_entity(
            db,
            entity_name=entity_name,
            entity_type=entity_type,
            limit=limit
        )
        
        return papers
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) 
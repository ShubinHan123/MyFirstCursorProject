from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List, Optional, Dict, Any
from app.models.models import Paper, Entity, papers_entities
from app.schemas.paper import PaperCreate
from app.schemas.entity import EntityCreate
import os

def get_paper(db: Session, paper_id: int) -> Optional[Paper]:
    return db.query(Paper).filter(Paper.paper_id == paper_id).first()

def get_papers(db: Session, skip: int = 0, limit: int = 100) -> List[Paper]:
    return db.query(Paper).offset(skip).limit(limit).all()

def create_paper(db: Session, paper: Dict[str, Any]) -> Paper:
    db_paper = Paper(
        paper_name=paper["paper_name"],
        paper_pdf=paper["paper_pdf"],
        paper_docx=paper["paper_docx"],
        paper_json=paper["paper_json"],
        paper_entities=paper["paper_entities"]
    )
    db.add(db_paper)
    db.commit()
    db.refresh(db_paper)
    return db_paper

def get_entity(db: Session, entity_id: int) -> Optional[Entity]:
    return db.query(Entity).filter(Entity.entity_id == entity_id).first()

def get_entities(db: Session, skip: int = 0, limit: int = 100) -> List[Dict[str, Any]]:
    """获取实体列表，包含每个实体关联的论文信息"""
    entities = db.query(Entity).offset(skip).limit(limit).all()
    
    result = []
    for entity in entities:
        # 获取与该实体关联的所有论文
        papers = db.query(Paper).join(papers_entities).filter(
            papers_entities.c.entity_id == entity.entity_id
        ).all()
        
        # 构建实体信息
        entity_info = {
            "entity_id": entity.entity_id,
            "entity_name": entity.entity_name,
            "entity_type": entity.entity_type,
            "papers": [
                {
                    "paper_id": paper.paper_id,
                    "paper_name": paper.paper_name,
                    # 获取该实体在这篇论文中出现的次数
                    "count": db.query(papers_entities.c.count).filter(
                        papers_entities.c.paper_id == paper.paper_id,
                        papers_entities.c.entity_id == entity.entity_id
                    ).scalar() or 0
                }
                for paper in papers
            ]
        }
        result.append(entity_info)
    
    return result

def create_entity(db: Session, entity: Dict[str, Any]) -> Entity:
    # 检查实体是否已存在
    existing_entity = db.query(Entity).filter(
        Entity.entity_name == entity["entity_name"],
        Entity.entity_type == entity["entity_type"]
    ).first()
    
    if existing_entity:
        return existing_entity
    
    db_entity = Entity(
        entity_name=entity["entity_name"],
        entity_type=entity["entity_type"]
    )
    db.add(db_entity)
    db.commit()
    db.refresh(db_entity)
    return db_entity

def add_paper_entity(db: Session, paper_id: int, entity_id: int, count: int = 1) -> None:
    # 检查关系是否已存在
    existing = db.query(papers_entities).filter_by(
        paper_id=paper_id,
        entity_id=entity_id
    ).first()
    
    if existing:
        # 更新计数
        stmt = papers_entities.update().where(
            papers_entities.c.paper_id == paper_id,
            papers_entities.c.entity_id == entity_id
        ).values(count=count)
        db.execute(stmt)
    else:
        # 创建新关系
        stmt = papers_entities.insert().values(
            paper_id=paper_id,
            entity_id=entity_id,
            count=count
        )
        db.execute(stmt)
    
    db.commit()

def search_entities(
    db: Session,
    query: str,
    entity_type: Optional[str] = None
) -> List[Entity]:
    search = db.query(Entity)
    if entity_type:
        search = search.filter(Entity.entity_type == entity_type)
    return search.filter(Entity.entity_name.ilike(f"%{query}%")).all()

def get_entity_statistics(db: Session) -> Dict[str, Any]:
    # 获取实体类型统计
    type_stats = db.query(
        Entity.entity_type,
        func.count(Entity.entity_id).label('count')
    ).group_by(Entity.entity_type).all()
    
    # 获取最常见的实体
    common_entities = db.query(
        Entity.entity_name,
        Entity.entity_type,
        func.count(papers_entities.c.paper_id).label('paper_count')
    ).join(papers_entities).group_by(
        Entity.entity_id
    ).order_by(
        func.count(papers_entities.c.paper_id).desc()
    ).limit(10).all()
    
    return {
        "type_statistics": [
            {"type": t[0], "count": t[1]} for t in type_stats
        ],
        "common_entities": [
            {
                "name": e[0],
                "type": e[1],
                "paper_count": e[2]
            } for e in common_entities
        ]
    }

def delete_paper(db: Session, paper_id: int) -> bool:
    """删除论文及其相关文件和关系"""
    try:
        # 获取论文信息（用于删除文件）
        paper = db.query(Paper).filter(Paper.paper_id == paper_id).first()
        if not paper:
            print(f"Paper with id {paper_id} not found")
            return False

        # 删除论文-实体关联关系
        result = db.query(papers_entities).filter(
            papers_entities.c.paper_id == paper_id
        ).delete(synchronize_session=False)
        print(f"Deleted {result} paper-entity relationships")

        # 删除相关文件
        files_to_delete = [
            paper.paper_pdf,
            paper.paper_docx,
            paper.paper_json,
            paper.paper_entities
        ]
        
        for file_path in files_to_delete:
            if file_path and os.path.exists(file_path):
                try:
                    os.remove(file_path)
                    print(f"Deleted file: {file_path}")
                except OSError as e:
                    print(f"Error deleting file {file_path}: {e}")
                    # 继续执行，不中断删除过程

        # 删除论文记录
        db.delete(paper)
        db.commit()
        print(f"Successfully deleted paper {paper_id}")
        return True
        
    except Exception as e:
        db.rollback()
        print(f"Error deleting paper {paper_id}: {e}")
        raise Exception(f"删除文档失败: {str(e)}")
    
    return False

def cleanup_unused_entities(db: Session) -> None:
    """删除没有关联论文的实体"""
    try:
        # 找到没有关联论文的实体
        unused_entities = db.query(Entity).filter(
            ~Entity.papers.any()
        ).all()
        
        # 删除这些实体
        for entity in unused_entities:
            db.delete(entity)
        
        db.commit()
    except Exception as e:
        db.rollback()
        print(f"Error cleaning up entities: {e}")

def search_papers_by_entity(
    db: Session,
    entity_name: str,
    entity_type: Optional[str] = None,
    limit: Optional[int] = None
) -> List[Paper]:
    """
    根据实体名称和类型搜索论文
    """
    query = db.query(Paper).distinct().join(
        papers_entities,
        Paper.paper_id == papers_entities.c.paper_id
    ).join(
        Entity,
        papers_entities.c.entity_id == Entity.entity_id
    ).filter(
        Entity.entity_name.ilike(f"%{entity_name}%")
    )
    
    if entity_type:
        query = query.filter(Entity.entity_type == entity_type)
    
    if limit:
        query = query.limit(limit)
    
    return query.all() 
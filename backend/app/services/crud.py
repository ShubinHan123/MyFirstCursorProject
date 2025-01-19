from sqlalchemy.orm import Session
from typing import List, Optional
from app.models.models import Paper, Entity
from app.schemas.paper import PaperCreate
from app.schemas.entity import EntityCreate

def get_paper(db: Session, paper_id: int) -> Optional[Paper]:
    return db.query(Paper).filter(Paper.paper_id == paper_id).first()

def get_papers(db: Session, skip: int = 0, limit: int = 100) -> List[Paper]:
    return db.query(Paper).offset(skip).limit(limit).all()

def create_paper(db: Session, paper: PaperCreate) -> Paper:
    db_paper = Paper(**paper.dict())
    db.add(db_paper)
    db.commit()
    db.refresh(db_paper)
    return db_paper

def get_entity(db: Session, entity_id: int) -> Optional[Entity]:
    return db.query(Entity).filter(Entity.entity_id == entity_id).first()

def get_entities(db: Session, skip: int = 0, limit: int = 100) -> List[Entity]:
    return db.query(Entity).offset(skip).limit(limit).all()

def create_entity(db: Session, entity: EntityCreate) -> Entity:
    db_entity = Entity(**entity.dict())
    db.add(db_entity)
    db.commit()
    db.refresh(db_entity)
    return db_entity

def search_entities(
    db: Session,
    query: str,
    entity_type: Optional[str] = None
) -> List[Entity]:
    search = db.query(Entity)
    if entity_type:
        search = search.filter(Entity.entity_type == entity_type)
    return search.filter(Entity.entity_name.ilike(f"%{query}%")).all() 
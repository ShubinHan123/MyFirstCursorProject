from sqlalchemy import Column, Integer, String, ForeignKey, Table
from sqlalchemy.orm import relationship
from app.db.base_class import Base

# 论文-实体关联表
papers_entities = Table(
    'papers_have_entities',
    Base.metadata,
    Column('paper_id', Integer, ForeignKey('papers.paper_id')),
    Column('entity_id', Integer, ForeignKey('entities.entity_id')),
    Column('count', Integer, default=1)
)

class Paper(Base):
    __tablename__ = "papers"

    paper_id = Column(Integer, primary_key=True, index=True)
    paper_name = Column(String, unique=True, index=True)
    paper_pdf = Column(String)
    paper_docx = Column(String)
    paper_json = Column(String)
    paper_entities = Column(String)
    
    # 与Entity的多对多关系
    entities = relationship(
        "Entity",
        secondary=papers_entities,
        back_populates="papers"
    )

class Entity(Base):
    __tablename__ = "entities"

    entity_id = Column(Integer, primary_key=True, index=True)
    entity_name = Column(String)
    entity_type = Column(String)
    
    # 与Paper的多对多关系
    papers = relationship(
        "Paper",
        secondary=papers_entities,
        back_populates="entities"
    ) 
from sqlalchemy import Column, Integer, String, Table, ForeignKey
from sqlalchemy.orm import relationship
from app.db.base_class import Base

# 论文-实体关联表
paper_entity = Table(
    'paper_entity',
    Base.metadata,
    Column('paper_id', Integer, ForeignKey('papers.id')),
    Column('entity_id', Integer, ForeignKey('entities.id'))
)

class Paper(Base):
    __tablename__ = "papers"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    pdf_path = Column(String)
    docx_path = Column(String)
    json_path = Column(String)
    entities_path = Column(String)
    
    # 关系
    entities = relationship("Entity", secondary=paper_entity, back_populates="papers")

class Entity(Base):
    __tablename__ = "entities"

    id = Column(Integer, primary_key=True, index=True)
    text = Column(String, index=True)
    label = Column(String, index=True)
    
    # 关系
    papers = relationship("Paper", secondary=paper_entity, back_populates="entities") 
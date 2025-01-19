from typing import List, Optional
from pydantic import BaseModel

class EntityBase(BaseModel):
    entity_name: str
    entity_type: str

class EntityCreate(EntityBase):
    pass

class Entity(EntityBase):
    entity_id: int
    
    class Config:
        orm_mode = True 
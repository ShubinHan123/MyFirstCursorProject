from typing import List, Optional
from pydantic import BaseModel

class PaperBase(BaseModel):
    paper_name: str
    paper_pdf: str
    paper_docx: str
    paper_json: str
    paper_entities: str

class PaperCreate(PaperBase):
    pass

class Paper(PaperBase):
    paper_id: int
    
    class Config:
        orm_mode = True 
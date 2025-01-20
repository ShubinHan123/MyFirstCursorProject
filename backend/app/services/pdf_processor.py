import os
import json
import spacy
from pdf2docx import parse
import docx
from simplify_docx import simplify
from app.core.config import settings
from app.schemas.entity import EntityCreate
from app.services import crud
from sqlalchemy.orm import Session

# 使用较小的英语模型
nlp = spacy.load("en_core_web_sm")

async def process_pdf(file_path: str, db: Session):
    """处理PDF文件并提取实体"""
    try:
        # 创建必要的目录
        os.makedirs("papers", exist_ok=True)
        os.makedirs("docs", exist_ok=True)
        os.makedirs("json", exist_ok=True)
        os.makedirs("ents", exist_ok=True)
        
        # 准备文件路径
        base_name = os.path.splitext(os.path.basename(file_path))[0]
        docx_path = os.path.join("docs", f"{base_name}.docx")
        json_path = os.path.join("json", f"{base_name}.json")
        ents_path = os.path.join("ents", f"{base_name}.json")
        
        # 转换PDF到DOCX
        parse(file_path, docx_path)
        
        # 读取DOCX文件
        doc = docx.Document(docx_path)
        
        # 保存简化的JSON
        with open(json_path, 'w', encoding='utf-8') as f:
            json.dump(simplify(doc, {"special-characters-as-text": False}), f)
        
        # 提取文本
        full_text = []
        for para in doc.paragraphs:
            if para.text.strip():  # 只处理非空段落
                full_text.append(para.text)
        
        # 实体识别
        full_doc = nlp(''.join(full_text))
        entities = {"entities": []}
        
        # 保存实体信息
        for ent in full_doc.ents:
            entity_info = {
                "text": ent.text,
                "start_char": ent.start_char,
                "end_char": ent.end_char,
                "label": ent.label_
            }
            entities["entities"].append(entity_info)
        
        with open(ents_path, 'w', encoding='utf-8') as f:
            json.dump(entities, f)
        
        # 创建论文记录
        paper_data = {
            "paper_name": base_name,
            "paper_pdf": file_path,
            "paper_docx": docx_path,
            "paper_json": json_path,
            "paper_entities": ents_path
        }
        paper = crud.create_paper(db, paper_data)
        
        # 处理实体
        entity_counts = {}  # 用于统计每个实体的出现次数
        for ent in entities["entities"]:
            entity_data = {
                "entity_name": ent["text"],
                "entity_type": ent["label"]
            }
            # 创建或获取实体
            entity = crud.create_entity(db, entity_data)
            
            # 更新实体计数
            key = (entity.entity_id, paper.paper_id)
            entity_counts[key] = entity_counts.get(key, 0) + 1
        
        # 批量更新实体关系和计数
        for (entity_id, paper_id), count in entity_counts.items():
            crud.add_paper_entity(db, paper_id, entity_id, count)
        
        return paper
        
    except Exception as e:
        # 清理临时文件
        for path in [docx_path, json_path, ents_path]:
            if os.path.exists(path):
                try:
                    os.remove(path)
                except:
                    pass
        raise Exception(f"处理PDF文件失败: {str(e)}") 
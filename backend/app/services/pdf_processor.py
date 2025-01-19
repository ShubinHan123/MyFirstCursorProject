import os
import json
import spacy
from pdf2docx import parse
import docx
from simplify_docx import simplify
from app.core.config import settings

nlp = spacy.load(settings.SPACY_MODEL)

async def process_pdf(pdf_path: str) -> dict:
    """
    处理PDF文件：
    1. 转换为DOCX
    2. 简化为JSON
    3. 提取实体
    """
    # 获取文件名（不含扩展名）
    base_name = os.path.splitext(os.path.basename(pdf_path))[0]
    
    # 创建必要的目录
    os.makedirs(settings.DOCS_DIR, exist_ok=True)
    os.makedirs(settings.JSON_DIR, exist_ok=True)
    os.makedirs(settings.ENTS_DIR, exist_ok=True)
    
    # 文件路径
    docx_path = os.path.join(settings.DOCS_DIR, f"{base_name}.docx")
    json_path = os.path.join(settings.JSON_DIR, f"{base_name}.json")
    ents_path = os.path.join(settings.ENTS_DIR, f"{base_name}.json")
    
    # 1. PDF转DOCX
    parse(pdf_path, docx_path)
    
    # 2. 读取DOCX并转换为JSON
    doc = docx.Document(docx_path)
    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(
            simplify(doc, {"special-characters-as-text": False}),
            f,
            ensure_ascii=False,
            indent=2
        )
    
    # 3. 提取文本内容
    full_text = []
    for para in doc.paragraphs:
        full_text.append(para.text)
    
    # 4. 实体识别
    entities = {"entities": []}
    doc = nlp(''.join(full_text))
    for ent in doc.ents:
        entities["entities"].append({
            "text": ent.text,
            "start_char": ent.start_char,
            "end_char": ent.end_char,
            "label": ent.label_
        })
    
    # 保存实体识别结果
    with open(ents_path, 'w', encoding='utf-8') as f:
        json.dump(entities, f, ensure_ascii=False, indent=2)
    
    # 返回文件信息
    return {
        "paper_name": base_name,
        "paper_pdf": pdf_path,
        "paper_docx": docx_path,
        "paper_json": json_path,
        "paper_entities": ents_path
    } 
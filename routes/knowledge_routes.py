from fastapi import APIRouter, HTTPException
from app.modules import Knowledge
from services.knowledge_service import KnowledgeService

router = APIRouter()


@router.post("/", response_model=Knowledge)
def create_knowledge(ks_id: str, knowledge: Knowledge):
    return KnowledgeService.create_knowledge(ks_id, knowledge)

@router.get("/{knowledge_id}", response_model=Knowledge)
def get_knowledge(ks_id: str, knowledge_id: str):
    return KnowledgeService.get_knowledge(ks_id, knowledge_id)

@router.put("/{knowledge_id}", response_model=Knowledge)
def update_knowledge(ks_id: str, knowledge_id: str, knowledge: Knowledge):
    return KnowledgeService.update_knowledge(ks_id, knowledge_id, knowledge)

@router.delete("/{knowledge_id}")
def delete_knowledge(ks_id: str, knowledge_id: str):
    return KnowledgeService.delete_knowledge(ks_id, knowledge_id)

@router.post("/search/")
def search_knowledge(ks_id: str, query: str):
    return KnowledgeService.search_knowledge(ks_id, query)

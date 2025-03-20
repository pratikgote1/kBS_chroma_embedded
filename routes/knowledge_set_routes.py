from fastapi import APIRouter, HTTPException
from app.modules import KnowledgeSet , Knowledge_Set
from services.knowledgeSet_service import KnowledgeSetService

router = APIRouter()


@router.post("/", response_model=KnowledgeSet)
def create_knowledge_set(ks: KnowledgeSet):
    return KnowledgeSetService.create_knowledge_set(ks)

@router.get("/{ks_id}", response_model=KnowledgeSet)
def get_knowledge_set(ks_id: str):
    return KnowledgeSetService.get_knowledge_set(ks_id)

@router.put("/{ks_id}", response_model=KnowledgeSet)
def update_knowledge_set(ks_id: str, ks: KnowledgeSet):
    return KnowledgeSetService.update_knowledge_set(ks_id, ks)

@router.delete("/{ks_id}")
def delete_knowledge_set(ks_id: str):
    return KnowledgeSetService.delete_knowledge_set(ks_id)
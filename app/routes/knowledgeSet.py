from fastapi import APIRouter
from app.models import KnowledgeSet
from app.services.knowledge_service import create_knowledge_set

router = APIRouter()

@router.post("/knowledge_set/")
def create_knowledge_set_route(data: KnowledgeSet):
    create_knowledge_set(data.name, data.description)
    return {"message": "Knowledge set created"}

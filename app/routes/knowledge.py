from fastapi import APIRouter
from app.models import  SearchRequest, Knowledge
from app.services.knowledge_service import add_knowledge, search_knowledge

router = APIRouter()

@router.post("/knowledge/")
def create_knowledge(data: Knowledge):
    add_knowledge(data.knowledge_set, data.text)
    return {"message": "Knowledge added successfully"}



@router.post("/knowledge/search/")
def search(data: SearchRequest):
     results = search_knowledge(data.knowledge_set, data.query, data.top_k)
     return {"results": results}



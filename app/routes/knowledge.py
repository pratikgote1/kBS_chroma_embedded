from fastapi import APIRouter, HTTPException, Query
from app.services.chroma_services import add_knowledge

router = APIRouter()

@router.post("/knowledge_sets/{knowledge_set_id}/knowledge/")
def add_knowledge_route(knowledge_set_id: str, text: str = Query(...)):
    try:
        response = add_knowledge(knowledge_set_id, text)
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

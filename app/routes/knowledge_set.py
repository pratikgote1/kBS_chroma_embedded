from fastapi import APIRouter, HTTPException
from app.models import KnowledgeSet
from app.services.chroma_services import create_knowledge_set, format_collection_name
from app.database import chroma_client

router = APIRouter()

@router.post("/knowledge_sets/")
def create_knowledge_set_route(knowledge_set: KnowledgeSet):
    try:
        response = create_knowledge_set(knowledge_set)
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/knowledge_sets/{knowledge_set_id}")
def read_knowledge_set(knowledge_set_id: str):
    collection = chroma_client.get_or_create_collection(name="my_knowledge_base")
    results = collection.get(ids=[knowledge_set_id])
    if not results or 'metadatas' not in results or not results['metadatas']:
        raise HTTPException(status_code=404, detail="Knowledge Set not found")
    knowledge_set_data = results['metadatas'][0]
    return KnowledgeSet(**knowledge_set_data)

@router.get("/knowledge_sets/")
def list_knowledge_sets():
    collection = chroma_client.get_or_create_collection(name="my_knowledge_base")
    results = collection.get()
    if 'metadatas' not in results:
        return []
    knowledge_sets = [KnowledgeSet(**metadata) for metadata in results['metadatas']]
    return knowledge_sets

@router.delete("/knowledge_sets/")
def delete_all_knowledge_sets():
    existing_collections = chroma_client.list_collections()
    for collection_name in existing_collections:
        chroma_client.delete_collection(collection_name)
    return {"detail": "All knowledge sets and their records have been deleted"}

@router.delete("/collections/")
def delete_all_collections():
    existing_collections = chroma_client.list_collections()
    for collection_name in existing_collections:
        chroma_client.delete_collection(collection_name)
    return {"detail": "All collections have been deleted"}

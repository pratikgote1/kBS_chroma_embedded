from fastapi import HTTPException
from app.database import collection
from services.embedding import get_embedding
from services.knowledgeSet_service import KnowledgeSetService

class KnowledgeService:
    @classmethod
    def create_knowledge(cls, ks_id, knowledge):
        if ks_id not in KnowledgeSetService.Knowledge_Set:
            raise HTTPException(status_code=404, detail="KnowledgeSet not found")
        ks = KnowledgeSetService.Knowledge_Set[ks_id]
        if any(k['knowledge_id'] == knowledge.knowledge_id for k in ks['knowledge']):
            raise HTTPException(status_code=400, detail="Knowledge already exists")
        knowledge.k_vector = get_embedding(knowledge.knowledge_text)
        ks['knowledge'].append(knowledge.dict())
        collection.add(knowledge.knowledge_id, knowledge.k_vector)
        return knowledge

    @classmethod
    def get_knowledge(cls, ks_id, knowledge_id):
        if ks_id not in KnowledgeSetService.Knowledge_Set:
            raise HTTPException(status_code=404, detail="KnowledgeSet not found")
        ks = KnowledgeSetService.Knowledge_Set[ks_id]
        for k in ks['knowledge']:
            if k['knowledge_id'] == knowledge_id:
                return k
        raise HTTPException(status_code=404, detail="Knowledge not found")

    @classmethod
    def update_knowledge(cls, ks_id, knowledge_id, knowledge):
        if ks_id not in KnowledgeSetService.Knowledge_Set:
            raise HTTPException(status_code=404, detail="KnowledgeSet not found")
        ks = KnowledgeSetService.Knowledge_Set[ks_id]
        for i, k in enumerate(ks['knowledge']):
            if k['knowledge_id'] == knowledge_id:
                knowledge.k_vector = get_embedding(knowledge.knowledge_text)
                ks['knowledge'][i] = knowledge.dict()
                collection.update(knowledge.knowledge_id, knowledge.k_vector)
                return knowledge
        raise HTTPException(status_code=404, detail="Knowledge not found")

    @classmethod
    def delete_knowledge(cls, ks_id, knowledge_id):
        if ks_id not in KnowledgeSetService.Knowledge_Set:
            raise HTTPException(status_code=404, detail="KnowledgeSet not found")
        ks = KnowledgeSetService.Knowledge_Set[ks_id]
        for i, k in enumerate(ks['knowledge']):
            if k['knowledge_id'] == knowledge_id:
                del ks['knowledge'][i]
                collection.delete(knowledge_id)
                return {"detail": "Knowledge deleted"}
        raise HTTPException(status_code=404, detail="Knowledge not found")

    @classmethod
    def search_knowledge(cls, ks_id, query):
        if ks_id not in KnowledgeSetService.Knowledge_Set:
            raise HTTPException(status_code=404, detail="KnowledgeSet not found")
        query_vector = get_embedding(query)
        results = collection.search(query_vector)
        return results
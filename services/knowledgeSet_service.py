from fastapi import HTTPException
#from app.database import collection
from typing import Dict


class KnowledgeSetService:
    Knowledge_Set: Dict[str, dict] = {}

    @classmethod
    def create_knowledge_set(cls, ks):
        if ks.ks_id in cls.Knowledge_Set:
            raise HTTPException(status_code=400, detail="KnowledgeSet already exists")
        cls.Knowledge_Set[ks.ks_id] = ks.dict()
        return ks

    @classmethod
    def get_knowledge_set(cls, ks_id):
        if ks_id not in cls.Knowledge_Set:
            raise HTTPException(status_code=404, detail="KnowledgeSet not found")
        return cls.Knowledge_Set[ks_id]

    @classmethod
    def update_knowledge_set(cls, ks_id, ks):
        if ks_id not in cls.Knowledge_Set:
            raise HTTPException(status_code=404, detail="KnowledgeSet not found")
        cls.Knowledge_Set[ks_id] = ks.dict()
        return ks

    @classmethod
    def delete_knowledge_set(cls, ks_id):
        if ks_id not in cls.Knowledge_Set:
            raise HTTPException(status_code=404, detail="KnowledgeSet not found")
        del cls.Knowledge_Set[ks_id]
        return {"detail": "KnowledgeSet deleted"}
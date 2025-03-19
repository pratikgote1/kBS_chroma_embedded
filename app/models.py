from pydantic import BaseModel
from typing import List, Dict

class Knowledge(BaseModel):
    id: str
    name_of_knowledge: str
    text: str
    vector: List[float] = None

class KnowledgeSet(BaseModel):
    id: str
    name: str
    description: str
    knowledge: List[Knowledge] = []

knowledge_sets: Dict[str, KnowledgeSet] = {}

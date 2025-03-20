from pydantic import BaseModel
from typing import List , Dict


class Knowledge(BaseModel):
    knowledge_id : str
    knowledge_name : str
    knowledge_text : str
    k_vector : List[float] = None
    
    
class KnowledgeSet(BaseModel):
    ks_id : str
    ks_name : str
    ks_description : str
    knowledge : List[Knowledge] = []
    
Knowledge_Set : Dict[str , KnowledgeSet] = {}
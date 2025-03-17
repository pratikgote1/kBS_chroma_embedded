from pydantic import BaseModel

class KnowledgeSet(BaseModel):
    name : str
    description : str
    
class Knowledge(BaseModel):
    knowledge_set : str
    text : str
    
class SearchRequest(BaseModel):
    knowledge_set : str
    text: str
    
# search request model
class SearchRequest(BaseModel):
    knowledge_set : str
    query : str
    top_k : int = 5
    
    
import chromadb

from app.database import chroma_client
from app.services.embedding import get_embedding


chroma_client = chromadb.PersistentClient(path="./chroma_db")
collection = chroma_client.get_or_create_collection(name = "my_knowledge_base")


def create_knowledge_set(name: str, description: str):
    chroma_client.create_collection(name)  


    
def add_knowledge(knowledge_set: str, text: str):
    embedding = get_embedding(text) 
    collection.add(
        ids=[knowledge_set + "_" + text[:10]],  
        embeddings = embedding, 
        metadatas=[{"knowledge_set": knowledge_set, "text": text}]
    )
    return {"message": "Knowledge added successfully"}



def search_knowledge(knowledge_set: str, query: str, top_k: int = 5):
    collection = chroma_client.get_collection(knowledge_set)
    query_embedding = get_embedding(query)
    results = collection.query(query_embeddings=[query_embedding], n_results=top_k)
    return results["documents"][0] 








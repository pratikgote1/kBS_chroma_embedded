import chromadb

from app.database import chroma_client
from app.services.embedding import get_embedding



chroma_client = chromadb.PersistentClient(path="./chroma_db")
collection = chroma_client.get_or_create_collection(name = "my_knowledge_base")



def format_collection_name(name: str) -> str:
    # Replace spaces with underscores
    formatted_name = name.replace(" ", "_")
    # Ensure the name is within the allowed length
    if len(formatted_name) < 3 or len(formatted_name) > 63:
        raise ValueError("Collection name must be between 3 and 63 characters")
    # Ensure the name starts and ends with an alphanumeric character
    if not (formatted_name[0].isalnum() and formatted_name[-1].isalnum()):
        raise ValueError("Collection name must start and end with an alphanumeric character")
    # Ensure the name contains only allowed characters
    for char in formatted_name:
        if not (char.isalnum() or char in ["_", "-"]):
            raise ValueError("Collection name contains invalid characters")
    return formatted_name


def add_knowledge(knowledge_set: str, text: str):
    embedding = get_embedding(text)
    print(embedding) 
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
    print(results)
    return results["documents"][0] 
   








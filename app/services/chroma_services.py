from app.database import chroma_client
from app.services.embedding import get_embedding

def format_collection_name(name: str) -> str:
    formatted_name = name.replace(" ", "_")
    if len(formatted_name) < 3 or len(formatted_name) > 63:
        raise ValueError("Collection name must be between 3 and 63 characters")
    if not (formatted_name[0].isalnum() and formatted_name[-1].isalnum()):
        raise ValueError("Collection name must start and end with an alphanumeric character")
    for char in formatted_name:
        if not (char.isalnum() or char in ["_", "-"]):
            raise ValueError("Collection name contains invalid characters")
    return formatted_name



def create_knowledge_set(knowledge_set):
    formatted_name = format_collection_name(knowledge_set.name)
    existing_collections = chroma_client.list_collections()
    if formatted_name in existing_collections:
        chroma_client.delete_collection(formatted_name)
    chroma_client.create_collection(formatted_name)
    collection = chroma_client.get_or_create_collection(name="my_knowledge_base")
    
    # Ensure metadata values are of the correct type
    metadata = knowledge_set.dict()
    for key, value in metadata.items():
        if isinstance(value, list):
            metadata[key] = str(value)  # Convert list to string
    
    collection.add(
        ids=[knowledge_set.id],
        metadatas=[metadata],
        documents=["dummy_document"]  # Add a dummy document to satisfy the API requirement
    )
    return knowledge_set


def add_knowledge(knowledge_set: str, text: str):
    embedding = get_embedding(text)
    collection = chroma_client.get_or_create_collection(name="my_knowledge_base")
    
    # Ensure metadata values are of the correct type
    metadata = {"knowledge_set": knowledge_set, "text": text}
    for key, value in metadata.items():
        if isinstance(value, list):
            metadata[key] = str(value)  # Convert list to string
    
    collection.add(
        ids=[knowledge_set + "_" + text[:10]],
        embeddings=embedding,
        metadatas=[metadata],
        documents=["dummy_document"]  # Add a dummy document to satisfy the API requirement
    )
    return {"message": "Knowledge added successfully"}



def search_knowledge(knowledge_set: str, query: str, top_k: int = 5):
    collection = chroma_client.get_collection(knowledge_set)
    query_embedding = get_embedding(query)
    results = collection.query(query_embeddings=[query_embedding], n_results=top_k)
    return results["documents"][0]

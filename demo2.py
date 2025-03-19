from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel
from typing import List, Dict
import chromadb
from app.services.embedding import get_embedding

app = FastAPI()

# Initialize ChromaDB PersistentClient
chroma_client = chromadb.PersistentClient(path="./chroma_db")
collection = chroma_client.get_or_create_collection(name="my_knowledge_base")

# Define the Knowledge and KnowledgeSet models
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

# Helper function to validate and format collection names
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

# CRUD operations for Knowledge Sets
@app.post("/knowledge_sets/")
def create_knowledge_set(knowledge_set: KnowledgeSet):
    formatted_name = format_collection_name(knowledge_set.name)
    
    # Check if the collection already exists in ChromaDB
    existing_collections = chroma_client.list_collections()
    if formatted_name in existing_collections:
        # Delete the existing collection
        chroma_client.delete_collection(formatted_name)
    
    # Create the collection in ChromaDB
    chroma_client.create_collection(formatted_name)
    
    # Add the knowledge set to ChromaDB
    collection.add(
        ids=[knowledge_set.id],
        metadatas=[knowledge_set.dict()]
    )
    
    return knowledge_set

@app.get("/knowledge_sets/{knowledge_set_id}")
def read_knowledge_set(knowledge_set_id: str):
    # Retrieve the knowledge set from ChromaDB
    results = collection.get(ids=[knowledge_set_id])
    if not results or 'metadatas' not in results or not results['metadatas']:
        raise HTTPException(status_code=404, detail="Knowledge Set not found")
    
    # Debugging statement to check the structure of results
    print(f"Results: {results}")
    
    # Access the metadata correctly
    knowledge_set_data = results['metadatas'][0]
    return KnowledgeSet(**knowledge_set_data)

@app.get("/knowledge_sets/")
def list_knowledge_sets():
    # Retrieve all knowledge sets from ChromaDB
    results = collection.get()
    
    # Debugging statement to check the structure of results
    print(f"Results: {results}")
    
    if 'metadatas' not in results:
        return []
    
    knowledge_sets = [KnowledgeSet(**metadata) for metadata in results['metadatas']]
    return knowledge_sets

# Endpoint to delete all records from the database
@app.delete("/knowledge_sets/")
def delete_all_knowledge_sets():
    existing_collections = chroma_client.list_collections()
    for collection_name in existing_collections:
        chroma_client.delete_collection(collection_name)
    return {"detail": "All knowledge sets and their records have been deleted"}

# New endpoint to delete all collections in ChromaDB
@app.delete("/collections/")
def delete_all_collections():
    existing_collections = chroma_client.list_collections()
    for collection_name in existing_collections:
        chroma_client.delete_collection(collection_name)
    return {"detail": "All collections have been deleted"}

# Endpoint to add knowledge to a knowledge set
@app.post("/knowledge_sets/{knowledge_set_id}/knowledge/")
def add_knowledge(knowledge_set_id: str, text: str = Query(...)):
    # Retrieve the knowledge set from ChromaDB
    results = collection.get(ids=[knowledge_set_id])
    if not results or 'metadatas' not in results or not results['metadatas']:
        raise HTTPException(status_code=404, detail="Knowledge Set not found")
    
    # Generate embedding for the text
    embedding = get_embedding(text)
    
    # Ensure the embedding is a list of lists of floats
    if hasattr(embedding, 'tolist'):
        embedding_list = embedding.tolist()
    else:
        embedding_list = embedding
    
    # Ensure the embedding_list is a list of lists
    if not isinstance(embedding_list[0], list):
        embedding_list = [embedding_list]
    
    # Convert any numpy arrays within the list to lists
    embedding_list = [[float(value) for value in sublist] for sublist in embedding_list]
    
    # Add knowledge to the collection
    collection.add(
        ids=[knowledge_set_id + "_" + text[:10]],
        embeddings=embedding_list,
        metadatas=[{"knowledge_set": knowledge_set_id, "text": text}]
    )
    
    # Update the knowledge set in ChromaDB
    knowledge_set_data = results['metadatas'][0]
    knowledge_set = KnowledgeSet(**knowledge_set_data)
    knowledge = Knowledge(id=knowledge_set_id + "_" + text[:10], name_of_knowledge=text[:10], text=text, vector=embedding_list[0])
    knowledge_set.knowledge.append(knowledge)
    
    collection.update(
        ids=[knowledge_set_id],
        metadatas=[knowledge_set.dict()]
    )
    
    return {"message": "Knowledge added successfully"}

# Run the application
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
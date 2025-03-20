import chromadb

try:
    chroma_client = chromadb.PersistentClient(path="./chroma_db")
    print("chromadb is connected")
except Exception as e:
    print(f"chroma db connection failed {e}")

collection = chroma_client.get_or_create_collection(name="my_knowledge_base")


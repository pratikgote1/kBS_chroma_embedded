from fastapi import FastAPI
from routes import knowledge_set_routes, knowledge_routes

app = FastAPI(title="Knowledge Management with chroma vector DB")

app.include_router(knowledge_set_routes.router, prefix="/knowledge_set", tags=["KnowledgeSet"])
app.include_router(knowledge_routes.router, prefix="/knowledge_set/{ks_id}/knowledge", tags=["Knowledge"])

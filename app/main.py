from fastapi import FastAPI
from app.routes import knowledge, knowledge_set

app = FastAPI(title="Knowledge Management API")

app.include_router(knowledge.router)
app.include_router(knowledge_set.router)

from fastapi import FastAPI
from app.routes import knowledge , knowledgeSet

app = FastAPI(title="Knowledge Management API")

app.include_router(knowledge.router)
app.include_router(knowledgeSet.router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
    
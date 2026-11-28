from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import leads

app = FastAPI(title="Lead Classifier API", version="2.0.0")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(leads.router)

@app.get("/health")
def health_check():
    return {"status": "healthy"}
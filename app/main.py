from fastapi import FastAPI
from app.routes import auth, documents

app = FastAPI()

# Uključivanje ruta za autentifikaciju i dokumente
app.include_router(auth.router, prefix="/auth", tags=["auth"])
app.include_router(documents.router, prefix="/docs", tags=["documents"])

@app.get("/")
def root():
    return {"message": "REST API za dokumente radi!"}

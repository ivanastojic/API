from fastapi import APIRouter, Depends, HTTPException, File, UploadFile
from app.utils.auth import verify_token
from app.utils.email_service import send_email
import shutil
import os

router = APIRouter()

UPLOAD_DIR = "uploaded_files"
os.makedirs(UPLOAD_DIR, exist_ok=True)

documents = {}

# Provjera prava korisnika (admin)
def check_admin_role(user: dict = Depends(verify_token)):
    if user["role"] != "admin":
        raise HTTPException(status_code=403, detail="Insufficient permissions")

# POST /documents - Upload dokumenta (samo za admin korisnike)
@router.post("/documents")
async def upload_document(file: UploadFile = File(...), current_user: dict = Depends(verify_token)):
    check_admin_role(current_user)
    
    file_path = os.path.join(UPLOAD_DIR, file.filename)  #putanja gdje ce se file cuvati
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)           #kopira se sadrzaj uploadanog file u file na serveru
    
    doc_id = len(documents) + 1
    documents[doc_id] = file.filename
    return {"id": doc_id, "filename": file.filename, "message": "Document uploaded successfully"}

# GET /documents/{id} - Dohvati dokument
@router.get("/documents/{id}")
async def get_document(id: int, current_user: dict = Depends(verify_token)):
    if id not in documents:
        raise HTTPException(status_code=404, detail="Document not found")
    return {"id": id, "filename": documents[id]}

# POST /documents/{id}/send - Slanje dokumenta na e-mail
@router.post("/documents/{id}/send")
async def send_document(id: int, recipient_email: str, current_user: dict = Depends(verify_token)):
    if id not in documents:
        raise HTTPException(status_code=404, detail="Document not found")
    
    file_path = os.path.join(UPLOAD_DIR, documents[id])   #putanja do filea
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="File not found")
    
    await send_email(recipient_email, "Your document", "Sending the requested document.", file_path)
    return {"message": f"Document sent to {recipient_email}"}

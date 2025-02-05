import os
import json
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.utils.auth import create_access_token

# Definiraj putanju do JSON datoteke
JSON_FILE = "data/fake_db.json"

# Osiguraj da JSON datoteka postoji
def ensure_json_file():
    if not os.path.exists(os.path.dirname(JSON_FILE)):
        os.makedirs(os.path.dirname(JSON_FILE))
    if not os.path.exists(JSON_FILE):
        with open(JSON_FILE, "w") as file:
            json.dump({}, file)  # Kreiraj prazan JSON objekt

# Funkcija za čitanje podataka iz JSON datoteke
def read_json_file():
    with open(JSON_FILE, "r") as file:
        return json.load(file)

# Funkcija za pisanje podataka u JSON datoteku
def write_json_file(data):
    with open(JSON_FILE, "w") as file:
        json.dump(data, file, indent=4)

# Inicijalizacija APIRouter-a
router = APIRouter()

# Modeli za zahtjeve
class RegisterUser(BaseModel):
    username: str
    password: str
    role: str  # Definiraj ulogu (npr. admin ili user)

class LoginRequest(BaseModel):
    username: str
    password: str

# POST /register - Registracija korisnika
@router.post("/register")
def register(user: RegisterUser):
    ensure_json_file()  # Osiguraj da datoteka postoji
    users = read_json_file()  # Učitaj trenutne korisnike iz datoteke

    if user.username in users:
        raise HTTPException(status_code=400, detail="Username already registered")
    
    # Dodaj korisnika u "bazu" (JSON)
    users[user.username] = {"password": user.password, "role": user.role}
    write_json_file(users)  # Spremi promjene u datoteku
    
    return {"msg": "User registered successfully"}

# POST /login - Prijava i generiranje JWT tokena
@router.post("/login")
async def login_for_access_token(form_data: LoginRequest):
    ensure_json_file()  # Osiguraj da datoteka postoji
    users = read_json_file()  # Učitaj korisnike iz JSON-a
    
    # Autentifikacija korisnika
    user = authenticate_user(users, form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    # Generiraj JWT token
    access_token = create_access_token(data={"sub": user["username"], "role": user["role"]})
    return {"access_token": access_token, "token_type": "bearer"}

# Funkcija za autentifikaciju korisnika
def authenticate_user(users: dict, username: str, password: str):
    user = users.get(username)
    if user and user["password"] == password:
        return {"username": username, "role": user["role"]}
    return None

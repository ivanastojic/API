from datetime import datetime, timedelta
from typing import Optional
from jose import JWTError, jwt
from fastapi import HTTPException

SECRET_KEY = "a_very_secret_key"  # Tajni ključ za potpisivanje tokena
ALGORITHM = "HS256"  # Algoritam za enkripciju
ACCESS_TOKEN_EXPIRE_MINUTES = 30  # Vrijeme isteka tokena u minutama

# Pomoćna funkcija za stvaranje JWT tokena
def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    
    to_encode.update({"exp": expire})   #dodaje kljuc exp koji ce biti kodiran u token
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

# Provjera korisničkih podataka
def authenticate_user(username: str, password: str):
    if username in fake_db:
        user = fake_db[username]
        if user["password"] == password:
            return {"username": username, "role": user["role"]}
    return None

# Verifikacija JWT tokena
def verify_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")

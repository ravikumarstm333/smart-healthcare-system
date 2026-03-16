from fastapi import APIRouter, HTTPException
from schemas.models import User
from database import users_collection
from passlib.context import CryptContext
import jwt
from datetime import datetime, timedelta
from config.settings import JWT_SECRET_KEY, ALGORITHM

router = APIRouter()
pwd_context = CryptContext(schemes=["pbkdf2_sha256"], deprecated="auto")

@router.post("/register")
def register_user(user: User):
    if users_collection.find_one({"username": user.username}):
        raise HTTPException(status_code=400, detail="Username already exists")
    hashed_password = pwd_context.hash(user.password)
    users_collection.insert_one({"username": user.username, "password": hashed_password})
    return {"message": "User created successfully"}

@router.post("/login")
def login_user(user: User):
    db_user = users_collection.find_one({"username": user.username})
    if not db_user or not pwd_context.verify(user.password, db_user["password"]):
        raise HTTPException(status_code=400, detail="Invalid username or password")
    
    encoded_jwt = jwt.encode(
        {"sub": user.username, "exp": datetime.utcnow() + timedelta(hours=24)},
        JWT_SECRET_KEY, 
        algorithm=ALGORITHM
    )
    return {"access_token": encoded_jwt, "token_type": "bearer", "username": user.username}

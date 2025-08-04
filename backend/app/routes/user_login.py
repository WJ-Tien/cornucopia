from app.core.database import db_manager
from app.schemas.user import UserLogin
from app.services.user import (
    create_valid_token, 
    verify_password 
)
from app.services.user import hash_password, get_username
from datetime import timedelta
from fastapi import APIRouter, HTTPException, status, Depends
from sqlalchemy.orm import Session

router = APIRouter()

@router.post("/login")
def login(user_login: UserLogin, db: Session = Depends(db_manager.get_db)):
    username = get_username(user_login.username, db)
    hashed_pwd = hash_password(user_login.password)
    if not username or not verify_password(user_login.password, hashed_pwd):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    access_token = create_valid_token(data={"username": username}, expires_delta=timedelta(minutes=30))
    refresh_token = create_valid_token(data={"username": username}, expires_delta=timedelta(days=7))
    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer"
    }
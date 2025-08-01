# User API routes
import jwt
from app.schemas.user import UserLogin
from app.services.user import (
    create_valid_token, 
    validate_access_token, 
    verify_password 
)
from datetime import timedelta
from fastapi import APIRouter, HTTPException, status
from app.services.user import hash_password, get_username


router = APIRouter()

@router.post("/login")
def login(user_login: UserLogin):
    # TODO
    user_id = get_username(user_login.username)
    hashed_pwd = hash_password(user_login.password)
    if not user_id or not verify_password(user_login.password, hashed_pwd):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    access_token = create_valid_token(data={"user_id": user_id}, expires_delta=timedelta(minutes=30))
    refresh_token = create_valid_token(data={"user_id": user_id}, expires_delta=timedelta(days=7))
    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer"
    }

@router.post("/refresh")
def refresh_access_token(refresh_token: str):
    try:
        payload = validate_access_token(refresh_token)
        user_id = payload.get("user_id")
        # 產生短效 access_token
        new_access_token = create_valid_token(
            data={"user_id": user_id}, 
            expires_delta=timedelta(minutes=30)  # 依你的安全需求調整
        )
        # 產生長效 refresh_token
        new_refresh_token = create_valid_token(
            data={"user_id": user_id}, 
            expires_delta=timedelta(days=7)
        )
        return {
            "access_token": new_access_token,
            "refresh_token": new_refresh_token,  # 取代舊的 refresh token
            "token_type": "bearer"
        }
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Refresh token expired")
    except jwt.PyJWTError:
        raise HTTPException(status_code=401, detail="Invalid refresh token")

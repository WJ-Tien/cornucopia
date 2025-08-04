import jwt
from app.services.user import (
    create_valid_token, 
    validate_access_token, 
)
from datetime import timedelta
from fastapi import APIRouter, HTTPException

router = APIRouter()

@router.post("/refresh")
def refresh_access_token(refresh_token: str):
    try:
        payload = validate_access_token(refresh_token)
        user_id = payload.get("username")
        # short-term access_token
        new_access_token = create_valid_token(
            data={"username": user_id}, 
            expires_delta=timedelta(minutes=30)  
        )
        # long-term refresh_token
        new_refresh_token = create_valid_token(
            data={"username": user_id}, 
            expires_delta=timedelta(days=7)
        )
        return {
            "access_token": new_access_token,
            "refresh_token": new_refresh_token,  # to replace the old one 
            "token_type": "bearer"
        }
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Refresh token expired")
    except jwt.PyJWTError:
        raise HTTPException(status_code=401, detail="Invalid refresh token")

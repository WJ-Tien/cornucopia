from app.core.database import db_manager
from app.schemas.user import UserLogin
from app.services.user import (
    create_valid_token, 
    verify_password 
)
from app.services.user import get_user_info
from app.core.security import csrf_protect
from app.utils.origin_check import validate_request_origin
from datetime import timedelta
from fastapi import APIRouter, HTTPException, status, Depends, Request, Response
from sqlalchemy.orm import Session

router = APIRouter()

@router.post("/login")
def login(
    user_login: UserLogin, 
    request: Request,
    response: Response,
    db: Session = Depends(db_manager.get_db)
):
    """User login - requires CSRF protection and origin validation"""
    # Validate request origin to prevent cross-site attacks
    validate_request_origin(request)
    
    # CSRF protection for state-changing operation
    csrf_protect.validate_csrf(request)
    
    user_info = get_user_info(user_login.username, db)
    hashed_pwd = user_info.hashed_password if user_info else ''
    if not user_info or not verify_password(user_login.password, hashed_pwd):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    
    # Short-lived access token (15 minutes)
    access_token = create_valid_token(data={"username": user_info.username}, expires_delta=timedelta(minutes=15))
    
    # Long-lived refresh token (7 days) stored in HttpOnly cookie
    refresh_token = create_valid_token(data={"username": user_info.username}, expires_delta=timedelta(days=7))
    
    # Set secure HttpOnly cookie for refresh token
    response.set_cookie(
        key="refresh_token",
        value=refresh_token,
        max_age=60 * 60 * 24 * 7,  # 7 days
        httponly=True,              # Prevent XSS access
        secure=False,               # Set to True in production with HTTPS
        samesite="lax",            # CSRF protection
        path="/cornucopia/user"     # Limit cookie scope
    )
    
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "username": user_info.username
    }
import jwt
from app.services.user import (
    create_valid_token, 
    validate_access_token, 
)
from datetime import timedelta
from fastapi import APIRouter, HTTPException, Request, Response

router = APIRouter()

@router.post("/refresh")
def refresh_access_token(
    request: Request,
    response: Response
):
    """Refresh access token using HttpOnly cookie - no CSRF needed for token refresh"""
    # Get refresh token from HttpOnly cookie
    refresh_token = request.cookies.get("refresh_token")
    
    if not refresh_token:
        raise HTTPException(status_code=401, detail="Refresh token missing")
    
    try:
        payload = validate_access_token(refresh_token)
        user_id = payload.get("username")
        
        if not user_id:
            raise HTTPException(status_code=401, detail="Invalid refresh token payload")
        
        # Generate new short-lived access token
        new_access_token = create_valid_token(
            data={"username": user_id}, 
            expires_delta=timedelta(minutes=15)  
        )
        
        # Generate new refresh token and update cookie
        new_refresh_token = create_valid_token(
            data={"username": user_id}, 
            expires_delta=timedelta(days=7)
        )
        
        # Update refresh token cookie
        response.set_cookie(
            key="refresh_token",
            value=new_refresh_token,
            max_age=60 * 60 * 24 * 7,  # 7 days
            httponly=True,              # Prevent XSS access
            secure=False,               # Set to True in production with HTTPS
            samesite="lax",            # CSRF protection
            path="/cornucopia/user"     # Limit cookie scope
        )
        
        return {
            "access_token": new_access_token,
            "token_type": "bearer"
        }
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Refresh token expired")
    except jwt.PyJWTError:
        raise HTTPException(status_code=401, detail="Invalid refresh token")

@router.post("/logout")
def logout(response: Response):
    """Logout user by clearing refresh token cookie"""
    response.delete_cookie(
        key="refresh_token",
        path="/cornucopia/user"
    )
    return {"message": "Logged out successfully"}

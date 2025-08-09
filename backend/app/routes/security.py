from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse
from ..core.security import csrf_protect

router = APIRouter(prefix="/security", tags=["security"])

@router.get("/csrf-token")
async def get_csrf_token(request: Request):
    """Get CSRF token for client
    
    This endpoint is safe to call without authentication.
    It generates a new CSRF token for the client to use in subsequent requests.
    
    Security considerations:
    - This endpoint doesn't require authentication (intentionally)
    - CSRF tokens are not secret, they prevent cross-site request forgery
    - Each call generates a fresh token with expiration
    - The token is also set as a secure cookie for double-submit pattern
    """
    csrf_token = csrf_protect.generate_csrf_token()
    response = JSONResponse({"csrf_token": csrf_token})
    csrf_protect.set_csrf_cookie(response, csrf_token)
    return response

from fastapi import HTTPException, Request

# Allowed origins for production and development
ALLOWED_ORIGINS = [
    "http://localhost:3000",    # React dev server (CRA)
    "http://localhost:5173",    # Vite dev server
    "https://your-domain.com",  # Production domain (update this)
]

def check_origin(request: Request) -> None:
    """
    Check if the request origin is allowed.
    Helps prevent CSRF and other cross-origin attacks.
    """
    origin = request.headers.get("origin")
    
    # Allow requests without Origin header (e.g., server-to-server, Postman)
    if not origin:
        return
    
    # Check if origin is in allowed list
    if origin not in ALLOWED_ORIGINS:
        raise HTTPException(
            status_code=403, 
            detail=f"Origin '{origin}' not allowed"
        )

def check_referer(request: Request) -> None:
    """
    Additional check for Referer header as backup.
    Some requests might not have Origin but have Referer.
    """
    referer = request.headers.get("referer")
    
    if not referer:
        return
    
    # Extract origin from referer URL
    try:
        from urllib.parse import urlparse
        parsed_referer = urlparse(referer)
        referer_origin = f"{parsed_referer.scheme}://{parsed_referer.netloc}"
        
        if referer_origin not in ALLOWED_ORIGINS:
            raise HTTPException(
                status_code=403,
                detail=f"Referer origin '{referer_origin}' not allowed"
            )
    except Exception:
        # If parsing fails, reject the request
        raise HTTPException(
            status_code=403,
            detail="Invalid referer header"
        )

def validate_request_origin(request: Request) -> None:
    """
    Combined origin validation using both Origin and Referer headers.
    Use this for state-changing operations.
    """
    try:
        check_origin(request)
        check_referer(request)
    except HTTPException:
        # If both checks fail, reject the request
        raise HTTPException(
            status_code=403,
            detail="Request origin validation failed"
        )

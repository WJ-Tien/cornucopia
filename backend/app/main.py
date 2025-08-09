import uvicorn
from app.routes.user_login import router as user_login_router
from app.routes.user_refresh_token import router as user_refresh_router
from app.routes.user_registration import router as user_register_router
from app.routes.cart import router as cart_router
from app.routes.cart_item import router as cart_item_router
from app.routes.security import router as security_router
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware


my_app = FastAPI(title="Cornucopia API", version="1.0.0", root_path="/cornucopia")

# Security headers middleware
@my_app.middleware("http")
async def add_security_headers(request: Request, call_next):
    response = await call_next(request)
    
    # Security headers
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["X-XSS-Protection"] = "1; mode=block"
    response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
    response.headers["Content-Security-Policy"] = (
        "default-src 'self'; "
        "script-src 'self'; "
        "style-src 'self' 'unsafe-inline'; "
        "img-src 'self' data: https:; "
        "connect-src 'self'; "
        "font-src 'self'; "
        "object-src 'none'; "
        "media-src 'self'; "
        "frame-src 'none'; "
        "base-uri 'self';"
    )
    
    return response

# CORS middleware with credentials support for HttpOnly cookies
my_app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:5173"],  # Specific origins
    allow_credentials=True,  # Required for HttpOnly cookies
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],  # Specific methods
    allow_headers=["Authorization", "Content-Type", "X-CSRF-Token"],  # Include CSRF header
)

# Include routers
my_app.include_router(security_router)  # Security endpoints (CSRF, etc.)
my_app.include_router(user_refresh_router, prefix="/user", tags=["user"])  
my_app.include_router(user_login_router, prefix="/user", tags=["user"])  
my_app.include_router(user_register_router, prefix="/user", tags=["user"])  
my_app.include_router(cart_router)  
my_app.include_router(cart_item_router) 

if __name__ == "__main__":
    uvicorn.run("app.main:my_app", host="0.0.0.0", port=8000, reload=True)

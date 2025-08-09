import secrets
import hmac
import hashlib
import time
from os import getenv
from typing import Optional
from fastapi import HTTPException, Request, Response

class CSRFProtection:
    """Custom CSRF protection implementation"""
    
    def __init__(self):
        self.secret_key = getenv("CSRF_SECRET_KEY", secrets.token_urlsafe(32))
        self.token_expiry = 3600  # 1 hour
        self.cookie_name = "csrftoken"
        self.header_name = "X-CSRF-Token"
    
    def generate_csrf_token(self) -> str:
        """Generate a CSRF token"""
        timestamp = str(int(time.time()))
        random_value = secrets.token_urlsafe(16)
        message = f"{timestamp}:{random_value}"
        
        signature = hmac.new(
            self.secret_key.encode(),
            message.encode(),
            hashlib.sha256
        ).hexdigest()
        
        return f"{message}:{signature}"
    
    def validate_csrf_token(self, token: str) -> bool:
        """Validate a CSRF token"""
        try:
            parts = token.split(":")
            if len(parts) != 3:
                return False
            
            timestamp, random_value, signature = parts
            message = f"{timestamp}:{random_value}"
            
            # Verify signature
            expected_signature = hmac.new(
                self.secret_key.encode(),
                message.encode(),
                hashlib.sha256
            ).hexdigest()
            
            if not hmac.compare_digest(signature, expected_signature):
                return False
            
            # Check expiry
            token_time = int(timestamp)
            current_time = int(time.time())
            
            if current_time - token_time > self.token_expiry:
                return False
            
            return True
        except (ValueError, TypeError):
            return False
    
    def set_csrf_cookie(self, response: Response, token: str):
        """Set CSRF token cookie"""
        response.set_cookie(
            key=self.cookie_name,
            value=token,
            max_age=self.token_expiry,
            httponly=False,  # Must be accessible to JavaScript
            secure=False,    # Set to True in production with HTTPS
            samesite="strict"
        )
    
    def get_csrf_token_from_request(self, request: Request) -> Optional[str]:
        """Get CSRF token from request (header or form data)"""
        # Try header first
        token = request.headers.get(self.header_name)
        if token:
            return token
        
        # Try cookie
        token = request.cookies.get(self.cookie_name)
        if token:
            return token
        
        return None
    
    def validate_csrf(self, request: Request):
        """Validate CSRF token from request"""
        token = self.get_csrf_token_from_request(request)
        
        if not token:
            raise HTTPException(
                status_code=403,
                detail="CSRF token missing"
            )
        
        if not self.validate_csrf_token(token):
            raise HTTPException(
                status_code=403,
                detail="Invalid or expired CSRF token"
            )

# Global CSRF protection instance
csrf_protect = CSRFProtection()

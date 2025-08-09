import html
import re
from typing import Optional

class InputSanitizer:
    """Input sanitization utilities to prevent XSS attacks"""
    
    @staticmethod
    def sanitize_text(text: Optional[str], max_length: Optional[int] = None) -> Optional[str]:
        """Sanitize text input by escaping HTML and trimming whitespace"""
        if text is None:
            return None
        
        # Strip leading/trailing whitespace
        text = text.strip()
        
        # Escape HTML characters to prevent XSS
        text = html.escape(text)
        
        # Limit length if specified
        if max_length and len(text) > max_length:
            text = text[:max_length]
        
        return text
    
    @staticmethod
    def sanitize_username(username: str) -> str:
        """Sanitize username with specific rules"""
        if not username:
            raise ValueError("Username cannot be empty")
        
        # Remove leading/trailing whitespace
        username = username.strip()
        
        # Only allow alphanumeric characters and underscores
        if not re.match(r'^[a-zA-Z0-9_]+$', username):
            raise ValueError("Username can only contain letters, numbers, and underscores")
        
        # Escape HTML just in case
        username = html.escape(username)
        
        # Length validation
        if len(username) < 3 or len(username) > 50:
            raise ValueError("Username must be between 3 and 50 characters")
        
        return username
    
    @staticmethod
    def sanitize_product_id(product_id: str) -> str:
        """Sanitize product ID"""
        if not product_id:
            raise ValueError("Product ID cannot be empty")
        
        product_id = product_id.strip()
        
        # Only allow alphanumeric characters, hyphens, and underscores
        if not re.match(r'^[a-zA-Z0-9_-]+$', product_id):
            raise ValueError("Product ID can only contain letters, numbers, hyphens, and underscores")
        
        # Escape HTML
        product_id = html.escape(product_id)
        
        # Length validation
        if len(product_id) > 100:
            raise ValueError("Product ID cannot exceed 100 characters")
        
        return product_id
    
    @staticmethod
    def sanitize_price(price_str: Optional[str]) -> Optional[str]:
        """Sanitize price string"""
        if price_str is None:
            return None
        
        price_str = price_str.strip()
        
        # Only allow digits, decimal point, and common currency symbols
        if not re.match(r'^[\d.,\$€£¥]+$', price_str):
            raise ValueError("Invalid price format")
        
        # Escape HTML
        price_str = html.escape(price_str)
        
        # Length validation
        if len(price_str) > 20:
            raise ValueError("Price string cannot exceed 20 characters")
        
        return price_str

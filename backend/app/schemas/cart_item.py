from pydantic import BaseModel, field_validator
from typing import Optional
from datetime import datetime
from ..utils.security import InputSanitizer

class CartItemBase(BaseModel):
    product_id: str
    quantity: int
    price_snapshot: Optional[str] = None
    
    @field_validator('product_id')
    @classmethod
    def validate_product_id(cls, v):
        return InputSanitizer.sanitize_product_id(v)
    
    @field_validator('price_snapshot')
    @classmethod
    def validate_price_snapshot(cls, v):
        return InputSanitizer.sanitize_price(v)
    
    @field_validator('quantity')
    @classmethod
    def validate_quantity(cls, v):
        if v < 0:
            raise ValueError("Quantity cannot be negative")
        if v > 10000:
            raise ValueError("Quantity cannot exceed 10000")
        return v

class CartItemCreate(CartItemBase):
    pass

class CartItemUpdate(BaseModel):
    quantity: Optional[int] = None
    price_snapshot: Optional[str] = None

class CartItem(CartItemBase):
    id: str
    cart_id: str
    created_at: datetime
    updated_at: datetime
    model_config = {
        "from_attributes": True
    }
    
# API request model
class AddToCartRequest(BaseModel):
    product_id: str
    quantity: int = 1
    price_snapshot: Optional[str] = None
    
    @field_validator('product_id')
    @classmethod
    def validate_product_id(cls, v):
        return InputSanitizer.sanitize_product_id(v)
    
    @field_validator('price_snapshot')
    @classmethod
    def validate_price_snapshot(cls, v):
        return InputSanitizer.sanitize_price(v)
    
    @field_validator('quantity')
    @classmethod
    def validate_quantity(cls, v):
        if v <= 0:
            raise ValueError("Quantity must be positive")
        if v > 10000:
            raise ValueError("Quantity cannot exceed 10000")
        return v

class UpdateCartItemRequest(BaseModel):
    quantity: int
    
    @field_validator('quantity')
    @classmethod
    def validate_quantity(cls, v):
        if v < 0:
            raise ValueError("Quantity cannot be negative")
        if v > 10000:
            raise ValueError("Quantity cannot exceed 10000")
        return v

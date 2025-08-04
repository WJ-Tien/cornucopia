from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class CartItemBase(BaseModel):
    product_id: str
    quantity: int
    price_snapshot: Optional[str] = None

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

class UpdateCartItemRequest(BaseModel):
    quantity: int

from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime
from .cart_item import CartItem

class CartBase(BaseModel):
    user_id: Optional[str] = None
    session_id: Optional[str] = None

class CartCreate(CartBase):
    pass

class Cart(CartBase):
    id: str
    items: List[CartItem] = []
    created_at: datetime
    updated_at: datetime

    model_config = {
        "from_attributes": True
    }

class CartResponse(BaseModel):
    cart: Cart
    total_items: int

    model_config = {
        "from_attributes": True
    }
    
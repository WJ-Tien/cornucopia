from typing import Optional
from sqlalchemy.orm import Session
from sqlalchemy import and_
from ..models.cart import Cart
from ..models.cart_item import CartItem
from ..schemas.cart_item import AddToCartRequest, UpdateCartItemRequest
from datetime import datetime, timezone

class CartItemService:
    
    @staticmethod
    def add_item_to_cart(
        db: Session, 
        cart: Cart, 
        request: AddToCartRequest
    ) -> CartItem:
        """Add item to cart"""
        # Check if the same product already exists
        existing_item = db.query(CartItem).filter(
            and_(
                CartItem.cart_id == cart.id,
                CartItem.product_id == request.product_id
            )
        ).first()
        
        if existing_item:
            # Update quantity
            existing_item.quantity += request.quantity
            existing_item.updated_at = datetime.now(timezone.utc)
            if request.price_snapshot:
                existing_item.price_snapshot = request.price_snapshot
            db.commit()
            db.refresh(existing_item)
            return existing_item
        else:
            # Create new cart item
            cart_item = CartItem(
                cart_id=cart.id,
                product_id=request.product_id,
                quantity=request.quantity,
                price_snapshot=request.price_snapshot
            )
            db.add(cart_item)
            db.commit()
            db.refresh(cart_item)
            return cart_item
    
    @staticmethod
    def update_cart_item(
        db: Session,
        cart_item_id: str,
        request: UpdateCartItemRequest,
        user_id: Optional[str] = None,
        session_id: Optional[str] = None
    ) -> Optional[CartItem]:
        """Update cart item"""
        # Build query conditions - simplified version
        query = db.query(CartItem).join(Cart).filter(CartItem.id == cart_item_id)
        
        if user_id:
            query = query.filter(Cart.user_id == user_id)
        elif session_id:
            query = query.filter(Cart.session_id == session_id)
        else:
            return None
            
        cart_item = query.first()
        if not cart_item:
            return None
            
        if request.quantity <= 0:
            # Delete item when quantity is 0 or negative
            db.delete(cart_item)
        else:
            cart_item.quantity = request.quantity
            cart_item.updated_at = datetime.now(timezone.utc)
            
        db.commit()
        return cart_item if request.quantity > 0 else None
    
    @staticmethod
    def remove_cart_item(
        db: Session,
        cart_item_id: str,
        user_id: Optional[str] = None,
        session_id: Optional[str] = None
    ) -> bool:
        """Remove item from cart"""
        query = db.query(CartItem).join(Cart).filter(CartItem.id == cart_item_id)
        
        if user_id:
            query = query.filter(Cart.user_id == user_id)
        elif session_id:
            query = query.filter(Cart.session_id == session_id)
        else:
            return False
            
        cart_item = query.first()
        if cart_item:
            db.delete(cart_item)
            db.commit()
            return True
        return False

from typing import Optional
from sqlalchemy.orm import Session, joinedload
from sqlalchemy import and_
from ..models.cart import Cart
from ..models.cart_item import CartItem
from datetime import datetime, timezone

class CartService:
    
    @staticmethod
    def get_or_create_cart(db: Session, user_id: Optional[str] = None, session_id: Optional[str] = None) -> Cart:
        """Get or create a cart - one user/session can only have one cart"""
        cart = None
        
        if user_id:
            # Logged in user: directly find the unique cart for the user with items preloaded
            cart = db.query(Cart).options(joinedload(Cart.items)).filter(Cart.user_id == user_id).first()
        elif session_id:
            # Anonymous user: find the unique cart for the session with items preloaded
            cart = db.query(Cart).options(joinedload(Cart.items)).filter(Cart.session_id == session_id).first()
            
        if not cart:
            # Create a new cart
            cart = Cart(
                user_id=user_id,
                session_id=session_id if not user_id else None
            )
            db.add(cart)
            try:
                db.commit()
                db.refresh(cart)
            except Exception as e:
                db.rollback()
                raise e
            
        return cart
    
    @staticmethod
    def get_cart(db: Session, user_id: Optional[str] = None, session_id: Optional[str] = None) -> Optional[Cart]:
        """Get cart for user or session with items preloaded"""
        if user_id:
            return db.query(Cart).options(joinedload(Cart.items)).filter(Cart.user_id == user_id).first()
        elif session_id:
            return db.query(Cart).options(joinedload(Cart.items)).filter(Cart.session_id == session_id).first()
        return None
    
    @staticmethod
    def clear_cart(
        db: Session,
        user_id: Optional[str] = None,
        session_id: Optional[str] = None
    ) -> bool:
        """clean the cart"""
        cart = CartService.get_cart(db, user_id, session_id)
        if cart:
            try:
                db.query(CartItem).filter(CartItem.cart_id == cart.id).delete()
                db.commit()
                return True
            except Exception as e:
                db.rollback()
                raise e
        return False
    
    @staticmethod
    def merge_carts(db: Session, user_id: str, session_id: str) -> Optional[Cart]:
        """Merge carts when user logs in - simplified version"""
        # Get user cart and anonymous cart with items preloaded
        user_cart = db.query(Cart).options(joinedload(Cart.items)).filter(Cart.user_id == user_id).first()
        anonymous_cart = db.query(Cart).options(joinedload(Cart.items)).filter(Cart.session_id == session_id).first()
        
        if not anonymous_cart:
            # No anonymous cart, return or create user cart
            return CartService.get_or_create_cart(db, user_id=user_id)
            
        if not user_cart:
            # User has no cart, directly convert anonymous cart to user cart
            anonymous_cart.user_id = user_id
            anonymous_cart.session_id = None
            anonymous_cart.updated_at = datetime.now(timezone.utc)
            try:
                db.commit()
                db.refresh(anonymous_cart)
                return anonymous_cart
            except Exception as e:
                db.rollback()
                raise e

        # Both carts exist, merge items into user cart
        for anonymous_item in anonymous_cart.items:
            existing_item = db.query(CartItem).filter(
                and_(
                    CartItem.cart_id == user_cart.id,
                    CartItem.product_id == anonymous_item.product_id
                )
            ).first()
            
            if existing_item:
                # Merge quantities
                existing_item.quantity += anonymous_item.quantity
                existing_item.updated_at = datetime.now(timezone.utc)
            else:
                # Move item to user cart
                anonymous_item.cart_id = user_cart.id

        # Delete anonymous cart
        try:
            db.delete(anonymous_cart)
            user_cart.updated_at = datetime.now(timezone.utc)
            db.commit()
            db.refresh(user_cart)
        except Exception as e:
            db.rollback()
            raise e
        
        return user_cart
    
    @staticmethod
    def get_cart_total_items(cart: Cart) -> int:
        """Calculate the total number of items in the cart"""
        return sum(item.quantity for item in cart.items)

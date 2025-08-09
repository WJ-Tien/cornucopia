import uuid
from fastapi import APIRouter, Depends, HTTPException, Request, Response
from sqlalchemy.orm import Session
from typing import Optional
from ..core.database import db_manager
from ..core.security import csrf_protect
from ..utils.origin_check import validate_request_origin
from ..services.cart import CartService
from ..services.cart_item import CartItemService
from ..services.user import get_current_user as _get_current_user
from ..schemas.cart import CartResponse
from ..schemas.cart_item import AddToCartRequest, UpdateCartItemRequest

router = APIRouter(prefix="/cart/items", tags=["cart-items"])

def get_db():
    """Get database connection"""
    return next(db_manager.get_db())

def get_current_user_optional() -> Optional[dict]:
    """Get current user (optional)"""
    try:
        return _get_current_user()
    except HTTPException:
        return None

def set_secure_cookie(response: Response, key: str, value: str):
    """Set secure cookie with improved security settings"""
    response.set_cookie(
        key=key,
        value=value,
        max_age=60*60*24*30,  # 30 days
        httponly=True,        # Prevent JavaScript access
        secure=False,         # Set to True in production with HTTPS
        samesite="strict"     # Strict CSRF protection
    )

def get_cart_identifier(request: Request, current_user: Optional[dict] = None):
    """Get cart identifier information"""
    if current_user:
        return {"user_id": str(current_user["id"]), "session_id": None}
    
    # For anonymous users, use session or cookie to identify
    session_id = request.cookies.get("cart_session_id")
    if not session_id:
        session_id = str(uuid.uuid4())
    
    return {"user_id": None, "session_id": session_id}

@router.post("/", response_model=CartResponse)
async def add_to_cart(
    request: Request,
    response: Response,
    add_request: AddToCartRequest,
    db: Session = Depends(get_db),
    current_user: Optional[dict] = Depends(get_current_user_optional)
):
    """Add product to cart - requires CSRF protection and origin validation"""
    # Validate request origin to prevent cross-site attacks
    validate_request_origin(request)
    
    # CSRF protection for state-changing operation
    csrf_protect.validate_csrf(request)
    
    cart_info = get_cart_identifier(request, current_user)
    
    # If anonymous user and no session_id, set cookie
    if not current_user and not request.cookies.get("cart_session_id"):
        set_secure_cookie(response, "cart_session_id", cart_info["session_id"])
    
    cart = CartService.get_or_create_cart(
        db, 
        user_id=cart_info["user_id"], 
        session_id=cart_info["session_id"]
    )
    
    CartItemService.add_item_to_cart(db, cart, add_request)
    
    # Refresh cart to get updated data
    db.refresh(cart)
    total_items = CartService.get_cart_total_items(cart)
    
    return CartResponse(cart=cart, total_items=total_items)

@router.put("/{item_id}", response_model=CartResponse)
async def update_cart_item(
    item_id: str,
    request: Request,
    update_request: UpdateCartItemRequest,
    db: Session = Depends(get_db),
    current_user: Optional[dict] = Depends(get_current_user_optional)
):
    """Update cart item quantity - requires CSRF protection and origin validation"""
    # Validate request origin to prevent cross-site attacks
    validate_request_origin(request)
    
    # CSRF protection for state-changing operation
    csrf_protect.validate_csrf(request)
    cart_info = get_cart_identifier(request, current_user)
    
    cart_item = CartItemService.update_cart_item(
        db,
        item_id,
        update_request,
        user_id=cart_info["user_id"],
        session_id=cart_info["session_id"]
    )
    
    if not cart_item and update_request.quantity > 0:
        raise HTTPException(status_code=404, detail="Cart item not found")
    
    # Get updated cart
    cart = CartService.get_cart(
        db, 
        user_id=cart_info["user_id"], 
        session_id=cart_info["session_id"]
    )
    
    if not cart:
        raise HTTPException(status_code=404, detail="Cart not found")
    
    total_items = CartService.get_cart_total_items(cart)
    
    return CartResponse(cart=cart, total_items=total_items)

@router.delete("/{item_id}")
async def remove_cart_item(
    item_id: str,
    request: Request,
    db: Session = Depends(get_db),
    current_user: Optional[dict] = Depends(get_current_user_optional)
):
    """Remove item from cart - requires CSRF protection and origin validation"""
    # Validate request origin to prevent cross-site attacks
    validate_request_origin(request)
    
    # CSRF protection for state-changing operation
    csrf_protect.validate_csrf(request)
    cart_info = get_cart_identifier(request, current_user)
    
    success = CartItemService.remove_cart_item(
        db,
        item_id,
        user_id=cart_info["user_id"],
        session_id=cart_info["session_id"]
    )
    
    if not success:
        raise HTTPException(status_code=404, detail="Cart item not found")
    
    return {"message": "Item removed from cart"}

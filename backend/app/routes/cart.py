import uuid
from fastapi import APIRouter, Depends, HTTPException, Request, Response
from sqlalchemy.orm import Session
from typing import Optional
from ..core.database import db_manager
from ..services.cart import CartService
from ..services.user import get_current_user as _get_current_user
from ..schemas.cart import CartResponse

router = APIRouter(prefix="/cart", tags=["cart"])

def get_db():
    """Get database connection"""
    return next(db_manager.get_db())

def get_current_user_optional() -> Optional[dict]:
    """Get current user (optional)"""
    try:
        return _get_current_user()
    except HTTPException:
        return None

def get_cart_identifier(request: Request, current_user: Optional[dict] = None):
    """Get cart identifier information"""
    if current_user:
        return {"user_id": str(current_user["id"]), "session_id": None}
    
    # For anonymous users, use session or cookie to identify
    session_id = request.cookies.get("cart_session_id")
    if not session_id:
        session_id = str(uuid.uuid4())
    
    return {"user_id": None, "session_id": session_id}

@router.get("/", response_model=CartResponse)
async def get_cart(
    request: Request,
    response: Response,
    db: Session = Depends(get_db),
    current_user: Optional[dict] = Depends(get_current_user_optional)
):
    """Get cart content"""
    cart_info = get_cart_identifier(request, current_user)
    
    # If anonymous user and no session_id, set cookie
    if not current_user and not request.cookies.get("cart_session_id"):
        response.set_cookie(
            key="cart_session_id", 
            value=cart_info["session_id"],
            max_age=60*60*24*30,  # 30 days
            httponly=True,
            samesite="lax"
        )
    
    cart = CartService.get_or_create_cart(
        db, 
        user_id=cart_info["user_id"], 
        session_id=cart_info["session_id"]
    )
    
    total_items = CartService.get_cart_total_items(cart)
    
    return CartResponse(cart=cart, total_items=total_items)

@router.delete("/")
async def clear_cart(
    request: Request,
    db: Session = Depends(get_db),
    current_user: Optional[dict] = Depends(get_current_user_optional)
):
    """Clear cart"""
    cart_info = get_cart_identifier(request, current_user)
    
    success = CartService.clear_cart(
        db,
        user_id=cart_info["user_id"],
        session_id=cart_info["session_id"]
    )
    
    if not success:
        raise HTTPException(status_code=404, detail="Cart not found")
    
    return {"message": "Cart cleared"}

@router.post("/merge")
async def merge_cart_on_login(
    request: Request,
    db: Session = Depends(get_db),
    current_user: dict = Depends(_get_current_user)  # Require login
):
    """Merge cart on user login"""
    session_id = request.cookies.get("cart_session_id")
    
    if not session_id:
        return {"message": "No anonymous cart to merge"}
    
    user_id = str(current_user["id"])
    merged_cart = CartService.merge_carts(db, user_id, session_id)
    
    if merged_cart:
        total_items = CartService.get_cart_total_items(merged_cart)
        return CartResponse(cart=merged_cart, total_items=total_items)
    
    return {"message": "No cart to merge"}

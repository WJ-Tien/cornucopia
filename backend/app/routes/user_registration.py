from app.core.database import db_manager
from app.schemas.user import UserCreate, UserOut
from app.services.user import create_user
from app.core.security import csrf_protect
from app.utils.origin_check import validate_request_origin
from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session

router = APIRouter()

@router.post("/register", response_model=UserOut, status_code=201)
def register_new_user(
    user_data: UserCreate, 
    request: Request,
    db: Session = Depends(db_manager.get_db)
):
    """Register new user - requires CSRF protection and origin validation"""
    # Validate request origin to prevent cross-site attacks
    validate_request_origin(request)
    
    # CSRF protection for state-changing operation
    csrf_protect.validate_csrf(request)
    
    try:
        new_user = create_user(db=db, user_data=user_data)
        return new_user
    except ValueError as e:
        raise HTTPException(
            status_code=400,
            detail=str(e),
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Internal Sever Error: {e}",
        )
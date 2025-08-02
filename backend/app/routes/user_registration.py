from app.core.database import get_db
from app.schemas.user import UserCreate, UserOut
from app.services.user import create_user
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session

router = FastAPI()

@router.post("/register", response_model=UserOut, status_code=201)
def register_new_user(user_data: UserCreate, db: Session = Depends(get_db)):
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
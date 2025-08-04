import bcrypt
import jwt
from app.models.user import User
from app.schemas.user import UserCreate
from datetime import datetime, timedelta, timezone
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from os import getenv
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
SECRET_KEY = getenv("CORNU_SECKEY") 
ALGORITHM = "HS256"

def get_user_info(username: str, db: Session) -> dict | None:
    """Placeholder function to get user by username."""
    user: User = db.query(User).filter(User.username == username).first()
    return user if user else None

def hash_password(password: str) -> bytes:
    pwd_bytes = password.encode('utf-8')
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password=pwd_bytes, salt=salt)
    return hashed_password

def verify_password(plain_password: str, hashed_password: str) -> bool:
    plain_password_bytes = plain_password.encode('utf-8')
    hashed_password_bytes = hashed_password.encode('utf-8')
    return bcrypt.checkpw(password=plain_password_bytes , hashed_password=hashed_password_bytes)

def create_valid_token(data: dict, expires_delta: timedelta = timedelta(hours=1)) -> str:
    """Generate a JWT access token, default expires in 1 hour."""
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + expires_delta
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def validate_access_token(token: str) -> dict:
    """Decode and validate JWT token, return payload. Raises exception if invalid."""
    return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])

def get_current_user(token: str = Depends(oauth2_scheme)) -> dict | None:
    # In a fastapi route
    # token: str = Depends(oauth2_scheme) --> extract token from HTTP header
    # and pass it to this function
    # Depends(get_current_user) --> use this function to get current user info (payload, dict)
    # no duplicate code in routes
    try:
        payload = validate_access_token(token)
        return payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Access token expired",
            headers={"WWW-Authenticate": "Bearer"},
        )
    except jwt.PyJWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid access token",
            headers={"WWW-Authenticate": "Bearer"},
        )

def create_user(db: Session, user_data: UserCreate):
    """
    register a new user in the database. 
    """

    hashed_pwd = hash_password(user_data.password).decode('utf-8')  # bcrypt returns bytes, decode to str for storage
    db_user = User(
        username=user_data.username,
        email=user_data.email,
        hashed_password=hashed_pwd
    )

    # add the user to the database session and ready to commit 
    db.add(db_user)

    try:
        db.commit()
        # refresh the session to get the new user object with ID
        db.refresh(db_user)
    except IntegrityError:
        db.rollback() 
        raise ValueError("usernmame or email already exists")
    except Exception:
        db.rollback() 
        raise 

    return db_user

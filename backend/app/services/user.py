import jwt
from datetime import datetime, timedelta, timezone
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from os import getenv
from passlib.context import CryptContext

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
SECRET_KEY = getenv("CORNU_SECKEY") 
ALGORITHM = "HS256"

def get_username(username: str) -> dict | None:
    # TODO: check if the username exists in the database
    """Placeholder function to get user by username."""
    return {"user_id": username} if username else None

def hash_password(password: str) -> str:
    """Hash a plain password for storing in the database."""
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a plain password against the hashed password from the database."""
    return pwd_context.verify(plain_password, hashed_password)

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

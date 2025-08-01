import jwt
from datetime import datetime, timedelta, timezone
from os import getenv
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
SECRET_KEY = getenv("CORNU_SECKEY") 
ALGORITHM = "HS256"

def hash_password(password: str) -> str:
    """Hash a plain password for storing in the database."""
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a plain password against the hashed password from the database."""
    return pwd_context.verify(plain_password, hashed_password)

def create_access_token(data: dict, expires_delta: timedelta = timedelta(hours=1)) -> str:
    """Generate a JWT access token, default expires in 1 hour."""
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + expires_delta
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def validate_access_token(token: str) -> dict:
    """Decode and validate JWT token, return payload. Raises exception if invalid."""
    return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])

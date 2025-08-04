import jwt
import pytest
from app.services import user
from datetime import datetime, timedelta, timezone
from fastapi import HTTPException

def test_hash_and_verify_password():
    password = "mysecretpassword"
    hashed = user.hash_password(password).decode('utf-8')
    assert hashed != password
    assert user.verify_password(password, hashed)
    assert not user.verify_password("wrongpassword", hashed)

def test_create_and_validate_access_token():
    data = {"username": "testuser"}
    token = user.create_valid_token(data, expires_delta=timedelta(minutes=5))
    assert isinstance(token, str)
    payload = user.validate_access_token(token)
    assert payload["username"] == "testuser"
    assert "exp" in payload

def test_validate_access_token_expired():
    data = {"username": "expireduser"}
    expired = datetime.now(timezone.utc) - timedelta(minutes=1)
    token = jwt.encode({**data, "exp": expired}, user.SECRET_KEY, algorithm=user.ALGORITHM)
    with pytest.raises(jwt.ExpiredSignatureError):
        user.validate_access_token(token)

def test_validate_access_token_invalid():
    data = {"username": "baduser"}
    token = jwt.encode({**data, "exp": datetime.now(timezone.utc) + timedelta(minutes=5)}, "WRONG_SECRET", algorithm=user.ALGORITHM)
    with pytest.raises(jwt.PyJWTError):
        user.validate_access_token(token)

def test_get_current_user_valid():
    data = {"username": "validuser"}
    token = user.create_valid_token(data, expires_delta=timedelta(minutes=5))
    result = user.get_current_user(token)
    assert result["username"] == "validuser"

def test_get_current_user_expired():
    data = {"username": "expireduser"}
    expired = datetime.now(timezone.utc) - timedelta(minutes=1)
    token = jwt.encode({**data, "exp": expired}, user.SECRET_KEY, algorithm=user.ALGORITHM)
    with pytest.raises(HTTPException) as excinfo:
        user.get_current_user(token)
    assert excinfo.value.status_code == 401
    assert excinfo.value.detail == "Access token expired"

def test_get_current_user_invalid():
    data = {"username": "baduser"}
    token = jwt.encode({**data, "exp": datetime.now(timezone.utc) + timedelta(minutes=5)}, "WRONG_SECRET", algorithm=user.ALGORITHM)
    with pytest.raises(HTTPException) as excinfo:
        user.get_current_user(token)
    assert excinfo.value.status_code == 401
    assert excinfo.value.detail == "Invalid access token"

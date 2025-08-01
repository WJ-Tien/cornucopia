from app.services import user
from datetime import timedelta

def test_hash_and_verify_password():
    password = "mysecretpassword"
    hashed = user.hash_password(password)
    assert hashed != password
    assert user.verify_password(password, hashed)
    assert not user.verify_password("wrongpassword", hashed)

def test_create_and_validate_access_token():
    data = {"user_id": "testuser"}
    token = user.create_access_token(data, expires_delta=timedelta(minutes=5))
    assert isinstance(token, str)
    payload = user.validate_access_token(token)
    assert payload["user_id"] == "testuser"
    assert "exp" in payload

from datetime import datetime
from pydantic import BaseModel, EmailStr, field_validator
from uuid import UUID
from ..utils.security import InputSanitizer

class UserBase(BaseModel):
    username: str
    email: EmailStr
    
    @field_validator('username')
    @classmethod
    def validate_username(cls, v):
        return InputSanitizer.sanitize_username(v)

class UserCreate(UserBase):
    password: str

class UserLogin(BaseModel):
    username: str
    password: str

# automatically generate the schema from the User model
# fastapi to sqlalchemy integration
# API response model
class UserOut(UserBase):
    id: UUID
    is_active: bool
    is_superuser: bool
    created_at: datetime
    updated_at: datetime

    model_config = {
        "from_attributes": True
    }
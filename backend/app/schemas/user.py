from datetime import datetime
from pydantic import BaseModel, EmailStr
from uuid import UUID

class UserBase(BaseModel):
    username: str
    email: EmailStr

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
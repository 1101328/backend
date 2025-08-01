from pydantic import BaseModel, EmailStr, Field, validator
from typing import Optional
from datetime import datetime

class UserCreateDTO(BaseModel):
    name: str = Field(min_length=2, max_length=32)
    email: EmailStr = Field(min_length=5, max_length=64)
    password: str = Field(min_length=8, max_length=32)
    memo: Optional[str] = None

class UserUpdateDTO(BaseModel):
    name: str | None = Field(min_length=2, max_length=32, default=None)
    password: str | None = Field(default=None)
    memo: Optional[str] = None

    @validator('password')
    def check_password_length(cls, v):
        if v is not None and len(v) < 8:
            raise ValueError('Password must be at least 8 characters')
        return v

class UserV0(BaseModel):
    id: str
    name: str
    email: str
    password: str
    memo: Optional[str] = None
    created_at: datetime
    updated_at: datetime

class GetUserResponse(BaseModel):
    total_count: int
    page: int
    users: list[UserV0]


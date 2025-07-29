from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import datetime

class UserCreateDTO(BaseModel):
    name: str = Field(min_length=2, max_length=32)
    email: EmailStr = Field(min_length=5, max_length=64)
    password: str = Field(min_length=8, max_length=32)
    memo: Optional[str] = None

class UserUpdateDTO(BaseModel):
    name: str | None = Field(min_length=2, max_length=32, default=None)
    password: str | None = Field(min_length=8, max_length=32, default=None) 
    memo: Optional[str] = None

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


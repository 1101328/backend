from dataclasses import dataclass
from datetime import datetime
from sqlalchemy.orm import Mapped, mapped_column
from pydantic import BaseModel

@dataclass
class User:
    id:str
    name: str
    email: str
    password:str
    memo: str | None
    created_at: datetime
    updated_at: datetime


@dataclass    
class UserV0(BaseModel):
    id: str
    name: str
    email: str
    password: str
    memo: str | None = None
    created_at: datetime
    updated_at: datetime

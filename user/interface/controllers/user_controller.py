from fastapi import APIRouter, Depends, Query
from dependency_injector.wiring import inject, Provide
from user.application.user_service import UserService
from user.domain.user import User
from user.interface.schemas import UserCreateDTO, UserUpdateDTO
from containers import Container
from user.interface.schemas import GetUserResponse
from pydantic import BaseModel, EmailStr, Field
from datetime import datetime
from fastapi.security import OAuth2PasswordRequestForm
from typing import Annotated
from common.auth import get_current_user, CurrentUser, get_admin_user

router = APIRouter(prefix="/users")  # ✅ prefix 설정

class CreateUserBody:
    name: str = Field(min_length=2, max_length=32)
    email: EmailStr = Field(max_length=64)
    password: str = Field(min_length=8, max_length=32)

class UpdateUserBody(BaseModel):
    name: str = Field(min_length=2, max_length=32, default=None)
    password: str = Field(min_length=8, max_length=32,default=None)

class UserResponse(BaseModel):
    id: str
    name: str
    email: str
    created_at: datetime
    updated_at: datetime    

@router.post("",status_code=201, response_model=UserResponse)
@inject
async def create_user(
    user_create: UserCreateDTO,
    user_service: UserService = Depends(Provide[Container.user_service])
):
    user: User = user_service.create_user(
        name=user_create.name,
        email=user_create.email,
        password=user_create.password,
        memo=user_create.memo
    )
    return user

@router.get("/{user_id}")
@inject
async def get_user_by_id(
    user_id: str,
    user_service: UserService = Depends(Provide[Container.user_service])
):
    user: User = user_service.get_user_by_id(user_id)
    return user

@router.get("/email/{email}")
@inject
async def get_user_by_email(
    email: str,
    user_service: UserService = Depends(Provide[Container.user_service])
):
    user: User = user_service.get_user_by_email(email)
    return user

@router.put("/{user_id}")
@inject
async def update_user(
    user_id: str,
    user_update: UserUpdateDTO,
    user_service: UserService = Depends(Provide[Container.user_service])
):
    updated_user: User = user_service.update_user(
        user_id=user_id,
        name=user_update.name,
        password=user_update.password,
        memo=user_update.memo
    )
    return updated_user

@router.get("")
@inject
def get_users(
    page: int = Query(1, ge=1), 
    items_per_page: int = Query(10, ge=1), 
    current_user: CurrentUser = Depends(get_admin_user),
    user_service: UserService = Depends(Provide[Container.user_service]),
) -> GetUserResponse:
    total_count, users = user_service.get_users(page, items_per_page)
    return {
        "total_count": total_count,
        "page": page,
        "users": [user.dict() for user in users],
    }


@router.delete("", status_code=204)
@inject
def delete_user(
    current_user: Annotated[CurrentUser, Depends(get_current_user)],
    user_service: UserService = Depends(Provide[Container.user_service]),
):
    user_service.delete_user(current_user.id)

@router.post("/login")
@inject
def login(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    user_service: UserService = Depends(Provide[Container.user_service])
):
    access_token = user_service.login(
        email=form_data.username,
        password=form_data.password
    )

    return {"access_token": access_token, "token_type": "bearer"}

@router.put("", response_model=UserResponse)
@inject
def update_user(
    current_user: Annotated[CurrentUser, Depends(get_current_user)],
    body: UpdateUserBody,
    user_service: UserService = Depends(Provide[Container.user_service]),
):
    user= user_service.update_user(
        user_id=current_user.id,
        name=body.name,
        password=body.password,
    )

    return user 


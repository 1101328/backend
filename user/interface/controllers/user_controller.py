from fastapi import APIRouter, Depends, Query
from dependency_injector.wiring import inject, Provide
from user.application.user_service import UserService
from user.domain.user import User
from user.interface.schemas import UserCreateDTO, UserUpdateDTO
from containers import Container
from user.interface.schemas import GetUserResponse

router = APIRouter(prefix="/users")  # ✅ prefix 설정

@router.post("")
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
    user_service: UserService = Depends(Provide[Container.user_service]),
) -> GetUserResponse:  # ✅ 여기에 추가!
    total_count, users = user_service.get_users(page, items_per_page)
    return {
        "total_count": total_count,
        "page": page,
        "users": [user.dict() for user in users],
    }


@router.delete("", status_code=204)
@inject
def delete_user(
    user_id: str = Query(..., description="삭제할 유저 ID"),
    user_service: UserService = Depends(Provide[Container.user_service]),
):
    user_service.delete_user(user_id)
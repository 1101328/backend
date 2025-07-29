from database import SessionLocal
from fastapi import HTTPException
from utils.db_utils import row_to_dict
from user.domain.repository.user_repo import IUserRepository
from user.domain.user import User as UserV0
from user.infra.db_models.user import User
from user.interface.schemas import UserV0  # ✅ 정확히 여기를 고쳐줘야 함



class UserRepository(IUserRepository):

    def save(self, user: UserV0):
        new_user = User(
            id=user.id,
            email=user.email,
            name=user.name,
            password=user.password,
            memo=user.memo,
            created_at=user.created_at,
            updated_at=user.updated_at
        )
        with SessionLocal() as db:
            db.add(new_user)
            db.commit()

    def find_by_email(self, email: str) -> UserV0:
        with SessionLocal() as db:
            user = db.query(User).filter(User.email == email).first()
            if not user:
                raise HTTPException(status_code=422, detail="User not found by email")
            return UserV0(**row_to_dict(user))

    def find_by_id(self, id: str) -> UserV0:
        with SessionLocal() as db:
            user = db.query(User).filter(User.id == id).first()
            if not user:
                raise HTTPException(status_code=422, detail="User not found by ID")
            return UserV0(**row_to_dict(user))

    def update(self, user_vo: UserV0) -> UserV0:
        with SessionLocal() as db:
            user = db.query(User).filter(User.id == user_vo.id).first()
            if not user:
                raise HTTPException(status_code=422, detail="User to update not found")

            user.name = user_vo.name
            user.password = user_vo.password
            user.memo = user_vo.memo
            user.updated_at = user_vo.updated_at

            db.commit()
            db.refresh(user)  # ✅ 변경사항 반영된 최신 상태로 동기화

            return UserV0(**row_to_dict(user))

    def get_users(self, page: int = 1, items_per_page: int = 10) -> tuple[int, list[UserV0]]:
        with SessionLocal() as db:
            query = db.query(User)
            total_count = query.count()
            offset = (page - 1) * items_per_page
            users = query.limit(items_per_page).offset(offset).all()

        return total_count, [UserV0(**row_to_dict(user)) for user in users]

    def delete(self, id: str):
        with SessionLocal() as db:
            user = db.query(User).filter(User.id == id).first()

            if not user:
                raise HTTPException(status_code=422)

            db.delete(user)
            db.commit()
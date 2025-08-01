from abc import ABCMeta, abstractmethod
from user.domain.user import User, UserV0
from typing import List, Tuple

class IUserRepository(metaclass=ABCMeta):

    @abstractmethod 
    def save(self, user: User):
        pass

    @abstractmethod
    def update(self, user: User):
        pass

    @abstractmethod
    def find_by_id(self, id: str) -> User:
        pass

    @abstractmethod
    def find_by_email(self, email: str) -> User:
        pass

    @abstractmethod
    def get_users(
        self, 
        page: int = 1,
        items_per_page: int = 10, 
    ) -> tuple[int, List[UserV0]]:
        raise NotImplementedError

    @abstractmethod
    def delete(self, id: str):
        raise NotImplementedError
        
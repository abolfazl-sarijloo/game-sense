from abc import ABC, abstractmethod
from typing import Optional
from uuid import UUID

from src.domain.entities.user import User


class UserRepository(ABC):

    @abstractmethod
    def create(self, user: User) -> User:
        raise NotImplementedError

    @abstractmethod
    def get_by_id(self, user_id: UUID) -> Optional[User]:
        raise NotImplementedError

    @abstractmethod
    def get_by_email(self, email: str) -> Optional[User]:
        raise NotImplementedError

    @abstractmethod
    def exists_by_email(self, email: str) -> bool:
        raise NotImplementedError
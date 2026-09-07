from abc import ABC, abstractmethod

from src.domain.entities.user import User


class TokenGenerator(ABC):

    @abstractmethod
    def generate_access_token(self, user: User) -> str:
        raise NotImplementedError
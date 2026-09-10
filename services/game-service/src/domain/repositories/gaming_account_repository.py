from abc import ABC, abstractmethod
from uuid import UUID

from src.domain.entities.gaming_account import GamingAccount


class GamingAccountRepository(ABC):

    @abstractmethod
    def get_by_user_and_game(
        self,
        user_id: UUID,
        game: str,
    ) -> GamingAccount | None:
        raise NotImplementedError

    @abstractmethod
    def get_by_id(
        self,
        account_id: int,
    ) -> GamingAccount | None:
        raise NotImplementedError

    @abstractmethod
    def save(
        self,
        account: GamingAccount,
    ) -> GamingAccount:
        raise NotImplementedError
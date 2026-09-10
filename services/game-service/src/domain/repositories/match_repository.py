from abc import ABC, abstractmethod

from src.domain.entities.match import Match


class MatchRepository(ABC):

    @abstractmethod
    def upsert(self, match: Match) -> Match:
        raise NotImplementedError

    @abstractmethod
    def get_by_account(
        self,
        gaming_account_id: int,
    ) -> list[Match]:
        raise NotImplementedError
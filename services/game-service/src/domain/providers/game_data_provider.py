from abc import ABC, abstractmethod


class GameDataProvider(ABC):

    @abstractmethod
    def get_player(
        self,
        account_id: str,
    ):
        raise NotImplementedError

    @abstractmethod
    def get_player_matches(
        self,
        account_id: str,
        limit: int = 20,
    ):
        raise NotImplementedError
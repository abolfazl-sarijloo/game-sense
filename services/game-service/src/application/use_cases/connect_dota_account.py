from src.domain.entities.gaming_account import GamingAccount
from src.domain.repositories.gaming_account_repository import (
    GamingAccountRepository,
)
from src.domain.providers.game_data_provider import GameDataProvider
from uuid import UUID


class ConnectDotaAccountUseCase:

    GAME = "dota2"
    PROVIDER = "stratz"

    def __init__(
        self,
        gaming_account_repository: GamingAccountRepository,
        game_data_provider: GameDataProvider,
    ):
        self.repository = gaming_account_repository
        self.provider = game_data_provider

    def execute(
        self,
        user_id: UUID,
        steam_account_id: int,
    ) -> GamingAccount:

        player = self.provider.get_player(
            steam_account_id
        )

        if not player.get("player"):
            raise ValueError(
                "Dota 2 account was not found."
            )

        existing = self.repository.get_by_user_and_game(
            user_id=user_id,
            game=self.GAME,
        )

        if existing:
            existing.external_id = steam_account_id
            return self.repository.save(existing)

        account = GamingAccount(
            id=None,
            user_id=user_id,
            game=self.GAME,
            provider=self.PROVIDER,
            external_id=steam_account_id,
        )

        return self.repository.save(account)
import os

from src.application.use_cases.connect_dota_account import (
    ConnectDotaAccountUseCase,
)
from src.application.use_cases.sync_dota_matches import (
    SyncDotaMatchesUseCase,
)
from src.infrastructure.persistence.repositories import (
    DjangoGamingAccountRepository,
    DjangoMatchRepository,
)
from src.infrastructure.providers.stratz.client import (
    StratzClient,
)
from src.infrastructure.providers.stratz.provider import (
    StratzProvider,
)


class Container:

    @staticmethod
    def get_stratz_provider() -> StratzProvider:

        token = os.getenv("STRATZ_TOKEN")

        if not token:
            raise RuntimeError(
                "STRATZ_TOKEN is not configured."
            )

        client = StratzClient(token)

        return StratzProvider(client)

    @staticmethod
    def get_connect_dota_account_use_case():

        repository = DjangoGamingAccountRepository()
        provider = Container.get_stratz_provider()

        return ConnectDotaAccountUseCase(
            gaming_account_repository=repository,
            game_data_provider=provider,
        )

    @staticmethod
    def get_sync_dota_matches_use_case():

        account_repository = DjangoGamingAccountRepository()
        match_repository = DjangoMatchRepository()
        provider = Container.get_stratz_provider()

        return SyncDotaMatchesUseCase(
            gaming_account_repository=account_repository,
            match_repository=match_repository,
            game_data_provider=provider,
        )
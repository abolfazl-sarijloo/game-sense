from datetime import datetime, timezone
from uuid import UUID

from src.domain.entities.match import Match
from src.domain.repositories.gaming_account_repository import (
    GamingAccountRepository,
)
from src.domain.repositories.match_repository import (
    MatchRepository,
)
from src.domain.providers.game_data_provider import GameDataProvider


class SyncDotaMatchesUseCase:

    def __init__(
        self,
        gaming_account_repository: GamingAccountRepository,
        match_repository: MatchRepository,
        game_data_provider: GameDataProvider,
    ):
        self.account_repository = gaming_account_repository
        self.match_repository = match_repository
        self.provider = game_data_provider

    def execute(
        self,
        user_id: UUID,
        limit: int = 20,
    ) -> dict:

        account = self.account_repository.get_by_user_and_game(
            user_id=user_id,
            game="dota2",
        )

        if not account:
            raise ValueError(
                "Dota 2 account is not connected."
            )

        matches = self.provider.get_player_matches(
            account_id=account.external_id,
            limit=limit,
        )

        synced = 0

        for data in matches:

            players = data.get("players") or []

            player = players[0] if players else {}

            start_time = data.get("startDateTime")

            parsed_start_time = None

            if start_time:
                try:
                    parsed_start_time = datetime.fromtimestamp(
                        start_time,
                        tz=timezone.utc,
                    )
                except (TypeError, ValueError):
                    parsed_start_time = None

            match = Match(
                id=None,
                gaming_account_id=account.id,
                external_match_id=int(data["id"]),
                hero_id=player.get("heroId"),
                kills=player.get("kills", 0),
                deaths=player.get("deaths", 0),
                assists=player.get("assists", 0),
                is_victory=player.get("isVictory"),
                duration_seconds=data.get("durationSeconds"),
                game_mode=data.get("gameMode"),
                start_time=parsed_start_time,
                raw_data=data,
            )

            self.match_repository.upsert(match)

            synced += 1

        return {
            "account_id": account.id,
            "synced": synced,
        }
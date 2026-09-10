from src.domain.entities.gaming_account import GamingAccount
from src.domain.entities.match import Match
from src.domain.repositories.gaming_account_repository import (
    GamingAccountRepository,
)
from src.domain.repositories.match_repository import MatchRepository

from uuid import UUID

from .models import GamingAccountModel, MatchModel


class DjangoGamingAccountRepository(GamingAccountRepository):

    def get_by_user_and_game(
        self,
        user_id: UUID,
        game: str,
    ) -> GamingAccount | None:

        model = (
            GamingAccountModel.objects
            .filter(user_id=user_id, game=game)
            .first()
        )

        if not model:
            return None

        return self._to_entity(model)

    def get_by_id(
        self,
        account_id: int,
    ) -> GamingAccount | None:

        model = (
            GamingAccountModel.objects
            .filter(id=account_id)
            .first()
        )

        if not model:
            return None

        return self._to_entity(model)

    def save(
        self,
        account: GamingAccount,
    ) -> GamingAccount:

        if account.id:
            model = GamingAccountModel.objects.get(
                id=account.id
            )

            model.user_id = account.user_id
            model.game = account.game
            model.provider = account.provider
            model.external_id = account.external_id

            model.save()

        else:
            model = GamingAccountModel.objects.create(
                user_id=account.user_id,
                game=account.game,
                provider=account.provider,
                external_id=account.external_id,
            )

        return self._to_entity(model)

    @staticmethod
    def _to_entity(
        model: GamingAccountModel,
    ) -> GamingAccount:

        return GamingAccount(
            id=model.id,
            user_id=model.user_id,
            game=model.game,
            provider=model.provider,
            external_id=model.external_id,
            created_at=model.created_at,
            updated_at=model.updated_at,
        )


class DjangoMatchRepository(MatchRepository):

    def upsert(self, match: Match) -> Match:

        model, _ = MatchModel.objects.update_or_create(
            gaming_account_id=match.gaming_account_id,
            external_match_id=match.external_match_id,
            defaults={
                "hero_id": match.hero_id,
                "kills": match.kills,
                "deaths": match.deaths,
                "assists": match.assists,
                "is_victory": match.is_victory,
                "duration_seconds": match.duration_seconds,
                "game_mode": match.game_mode,
                "start_time": match.start_time,
                "raw_data": match.raw_data,
            },
        )

        return self._to_entity(model)

    def get_by_account(
        self,
        gaming_account_id: int,
    ) -> list[Match]:

        models = (
            MatchModel.objects
            .filter(gaming_account_id=gaming_account_id)
            .order_by("-start_time")
        )

        return [
            self._to_entity(model)
            for model in models
        ]

    @staticmethod
    def _to_entity(
        model: MatchModel,
    ) -> Match:

        return Match(
            id=model.id,
            gaming_account_id=model.gaming_account_id,
            external_match_id=model.external_match_id,
            hero_id=model.hero_id,
            kills=model.kills,
            deaths=model.deaths,
            assists=model.assists,
            is_victory=model.is_victory,
            duration_seconds=model.duration_seconds,
            game_mode=model.game_mode,
            start_time=model.start_time,
            raw_data=model.raw_data,
            created_at=model.created_at,
            updated_at=model.updated_at,
        )
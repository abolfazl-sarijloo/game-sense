from src.domain.providers.game_data_provider import GameDataProvider

from .client import StratzClient


class StratzProvider(GameDataProvider):

    def __init__(self, client: StratzClient):
        self.client = client

    def get_player(
        self,
        account_id: int,
    ) -> dict:

        query = """
        query GetPlayer($steamAccountId: Long!) {
            player(
                steamAccountId: $steamAccountId
            ) {
                steamAccountId
            }
        }
        """

        return self.client.execute(
            query=query,
            variables={
                "steamAccountId": account_id,
            },
        )

    def get_player_matches(
        self,
        account_id: int,
        limit: int = 20,
    ) -> list[dict]:

        query = """
        query GetPlayerMatches(
            $steamAccountId: Long!
            $take: Int!
        ) {
            player(
                steamAccountId: $steamAccountId
            ) {
                matches(
                    request: {
                        take: $take
                    }
                ) {
                    id
                    startDateTime
                    durationSeconds
                    gameMode
                    players(
                        steamAccountId: $steamAccountId
                    ) {
                        steamAccountId
                        heroId
                        kills
                        deaths
                        assists
                        isVictory
                    }
                }
            }
        }
        """

        result = self.client.execute(
            query=query,
            variables={
                "steamAccountId": account_id,
                "take": limit,
            },
        )

        player = result.get("player")

        if not player:
            return []

        return player.get("matches", [])
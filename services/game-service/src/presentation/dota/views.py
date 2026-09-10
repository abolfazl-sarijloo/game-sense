from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from src.infrastructure.di.container import Container

from .serializers import (
    ConnectDotaAccountSerializer,
    SyncDotaMatchesSerializer,
)


class ConnectDotaAccountView(APIView):

    permission_classes = [IsAuthenticated]

    def post(self, request):

        serializer = ConnectDotaAccountSerializer(
            data=request.data
        )

        serializer.is_valid(raise_exception=True)

        use_case = (
            Container
            .get_connect_dota_account_use_case()
        )

        try:

            account = use_case.execute(
                user_id=request.user.id,
                steam_account_id=serializer.validated_data[
                    "steam_account_id"
                ],
            )

        except ValueError as exc:

            return Response(
                {"error": str(exc)},
                status=400,
            )

        return Response(
            {
                "id": account.id,
                "game": account.game,
                "provider": account.provider,
                "external_id": account.external_id,
                "status": "connected",
            },
            status=200,
        )


class SyncDotaMatchesView(APIView):

    permission_classes = [IsAuthenticated]

    def post(self, request):

        serializer = SyncDotaMatchesSerializer(
            data=request.data
        )

        serializer.is_valid(raise_exception=True)

        use_case = (
            Container
            .get_sync_dota_matches_use_case()
        )

        try:

            result = use_case.execute(
                user_id=request.user.id,
                limit=serializer.validated_data[
                    "limit"
                ],
            )

        except ValueError as exc:

            return Response(
                {"error": str(exc)},
                status=400,
            )

        return Response(result)


class DotaAccountView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):

        repository = (
            Container
            .get_connect_dota_account_use_case()
            .repository
        )

        account = repository.get_by_user_and_game(
            user_id=request.user.id,
            game="dota2",
        )

        if not account:
            return Response(
                {
                    "error": "Dota 2 account is not connected."
                },
                status=404,
            )

        return Response(
            {
                "id": account.id,
                "game": account.game,
                "provider": account.provider,
                "external_id": account.external_id,
            }
        )


class DotaMatchesView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):

        account_repository = (
            Container
            .get_sync_dota_matches_use_case()
            .account_repository
        )

        match_repository = (
            Container
            .get_sync_dota_matches_use_case()
            .match_repository
        )

        account = account_repository.get_by_user_and_game(
            user_id=request.user.id,
            game="dota2",
        )

        if not account:
            return Response(
                {
                    "error": "Dota 2 account is not connected."
                },
                status=404,
            )

        matches = match_repository.get_by_account(
            account.id
        )

        return Response(
            [
                {
                    "id": match.id,
                    "external_match_id": (
                        match.external_match_id
                    ),
                    "hero_id": match.hero_id,
                    "kills": match.kills,
                    "deaths": match.deaths,
                    "assists": match.assists,
                    "is_victory": match.is_victory,
                    "duration_seconds": (
                        match.duration_seconds
                    ),
                    "game_mode": match.game_mode,
                    "start_time": (
                        match.start_time
                    ),
                }
                for match in matches
            ]
        )
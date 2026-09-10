from rest_framework import serializers


class ConnectDotaAccountSerializer(
    serializers.Serializer
):
    steam_account_id = serializers.IntegerField(
        min_value=1
    )


class SyncDotaMatchesSerializer(
    serializers.Serializer
):
    limit = serializers.IntegerField(
        min_value=1,
        max_value=100,
        required=False,
        default=20,
    )
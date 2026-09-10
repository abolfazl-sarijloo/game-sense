from django.db import models


class GamingAccountModel(models.Model):

    GAME_DOTA2 = "dota2"
    PROVIDER_STRATZ = "stratz"

    GAME_CHOICES = [
        (GAME_DOTA2, "Dota 2"),
    ]

    PROVIDER_CHOICES = [
        (PROVIDER_STRATZ, "STRATZ"),
    ]

    user_id = models.UUIDField(db_index=True)
    game = models.CharField(
        max_length=50,
        choices=GAME_CHOICES,
    )
    provider = models.CharField(
        max_length=50,
        choices=PROVIDER_CHOICES,
    )
    external_id = models.BigIntegerField()

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "gaming_accounts"
        constraints = [
            models.UniqueConstraint(
                fields=["user_id", "game"],
                name="unique_user_game",
            )
        ]

    def __str__(self):
        return f"{self.user_id} - {self.game}"


class MatchModel(models.Model):

    gaming_account = models.ForeignKey(
        GamingAccountModel,
        on_delete=models.CASCADE,
        related_name="matches",
    )

    external_match_id = models.BigIntegerField()

    hero_id = models.IntegerField(
        null=True,
        blank=True,
    )

    kills = models.IntegerField(default=0)
    deaths = models.IntegerField(default=0)
    assists = models.IntegerField(default=0)

    is_victory = models.BooleanField(
        null=True,
        blank=True,
    )

    duration_seconds = models.IntegerField(
        null=True,
        blank=True,
    )

    game_mode = models.IntegerField(
        null=True,
        blank=True,
    )

    start_time = models.DateTimeField(
        null=True,
        blank=True,
    )

    raw_data = models.JSONField(default=dict)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "matches"
        constraints = [
            models.UniqueConstraint(
                fields=[
                    "gaming_account",
                    "external_match_id",
                ],
                name="unique_account_match",
            )
        ]

    def __str__(self):
        return str(self.external_match_id)
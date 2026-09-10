from django.urls import path

from .views import (
    ConnectDotaAccountView,
    DotaAccountView,
    DotaMatchesView,
    SyncDotaMatchesView,
)


urlpatterns = [
    path(
        "connect/",
        ConnectDotaAccountView.as_view(),
        name="dota-connect",
    ),
    path(
        "sync/",
        SyncDotaMatchesView.as_view(),
        name="dota-sync",
    ),
    path(
        "account/",
        DotaAccountView.as_view(),
        name="dota-account",
    ),
    path(
        "matches/",
        DotaMatchesView.as_view(),
        name="dota-matches",
    ),
]
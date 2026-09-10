from dataclasses import dataclass
from datetime import datetime
from typing import Any


@dataclass
class Match:
    id: int | None
    gaming_account_id: int
    external_match_id: int
    hero_id: int | None
    kills: int
    deaths: int
    assists: int
    is_victory: bool | None
    duration_seconds: int | None
    game_mode: int | None
    start_time: datetime | None
    raw_data: dict[str, Any]
    created_at: datetime | None = None
    updated_at: datetime | None = None
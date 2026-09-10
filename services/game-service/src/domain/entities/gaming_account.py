from dataclasses import dataclass
from datetime import datetime
from uuid import UUID


@dataclass
class GamingAccount:
    id: int | None
    user_id: UUID
    game: str
    provider: str
    external_id: int
    created_at: datetime | None = None
    updated_at: datetime | None = None
from dataclasses import dataclass
from datetime import datetime, timezone
from uuid import UUID, uuid4


@dataclass
class User:
    id: UUID
    username: str
    email: str
    password_hash: str
    created_at: datetime
    updated_at: datetime

    @classmethod
    def create(
        cls,
        username: str,
        email: str,
        password_hash: str,
    ) -> "User":
        now = datetime.now(timezone.utc)

        return cls(
            id=uuid4(),
            username=username,
            email=email,
            password_hash=password_hash,
            created_at=now,
            updated_at=now,
        )
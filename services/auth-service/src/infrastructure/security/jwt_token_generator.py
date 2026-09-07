from datetime import datetime, timedelta, timezone

import jwt
from django.conf import settings

from src.domain.entities.user import User
from src.domain.repositories.token_generator import TokenGenerator


class JWTTokenGenerator(TokenGenerator):

    def generate_access_token(self, user: User) -> str:
        now = datetime.now(timezone.utc)

        expires_at = now + timedelta(
            minutes=settings.JWT_ACCESS_TOKEN_LIFETIME_MINUTES
        )

        payload = {
            "sub": str(user.id),
            "email": user.email,
            "type": "access",
            "iat": now,
            "exp": expires_at,
        }

        return jwt.encode(
            payload,
            settings.SECRET_KEY,
            algorithm=settings.JWT_ALGORITHM,
        )
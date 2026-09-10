import jwt
from uuid import UUID
from django.conf import settings
from rest_framework import authentication
from rest_framework.exceptions import AuthenticationFailed


class AuthenticatedUser:
    """Lightweight user object for cross-service JWT auth.

    game-service has no users table, so we don't hit the DB here.
    The token is issued by auth-service; we only validate it.
    """

    def __init__(self, user_id, email=None):
        self.id = user_id
        self.email = email

    @property
    def is_authenticated(self):
        return True

    @property
    def is_anonymous(self):
        return False


class JWTAuthentication(authentication.BaseAuthentication):
    def authenticate(self, request):
        auth_header = request.headers.get("Authorization")

        if not auth_header:
            return None

        parts = auth_header.split()

        if len(parts) != 2 or parts[0].lower() != "bearer":
            raise AuthenticationFailed("Invalid authorization header.")

        token = parts[1]

        try:
            payload = jwt.decode(
                token,
                settings.JWT_SECRET,
                algorithms=[settings.JWT_ALGORITHM],
            )
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed("Token has expired.")
        except jwt.InvalidTokenError:
            raise AuthenticationFailed("Invalid token.")

        if payload.get("type") != "access":
            raise AuthenticationFailed("Invalid token type.")

        raw_user_id = payload.get("sub")

        if not raw_user_id:
            raise AuthenticationFailed("Invalid token.")

        try:
            user_id = UUID(str(raw_user_id))
        except (ValueError, AttributeError, TypeError):
            raise AuthenticationFailed("Invalid token.")

        user = AuthenticatedUser(
            user_id=user_id,
            email=payload.get("email"),
        )

        return (user, token)

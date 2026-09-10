import jwt

from django.conf import settings
from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed


class JWTAuthentication(BaseAuthentication):

    def authenticate(self, request):
        auth_header = request.headers.get("Authorization")

        if not auth_header:
            return None

        try:
            scheme, token = auth_header.split(" ", 1)
        except ValueError:
            raise AuthenticationFailed(
                "Invalid authorization header."
            )

        if scheme.lower() != "bearer":
            raise AuthenticationFailed(
                "Authorization scheme must be Bearer."
            )

        try:
            payload = jwt.decode(
                token,
                settings.JWT_SECRET,
                algorithms=["HS256"],
            )
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed(
                "Token has expired."
            )
        except jwt.InvalidTokenError:
            raise AuthenticationFailed(
                "Invalid token."
            )

        user_id = payload.get("user_id") or payload.get("sub")

        if not user_id:
            raise AuthenticationFailed(
                "Token does not contain user identity."
            )

        return (
            GameSenseUser(
                user_id=int(user_id),
            ),
            token,
        )


class GameSenseUser:

    def __init__(self, user_id: int):
        self.id = user_id

    @property
    def is_authenticated(self):
        return True
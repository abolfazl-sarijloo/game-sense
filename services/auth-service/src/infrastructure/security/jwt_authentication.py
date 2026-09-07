import jwt

from django.conf import settings
from rest_framework import authentication
from rest_framework.exceptions import AuthenticationFailed

from src.presentation.users.models import UserModel


class JWTAuthentication(authentication.BaseAuthentication):

    def authenticate(self, request):

        auth_header = request.headers.get("Authorization")

        if not auth_header:
            return None

        parts = auth_header.split()

        if len(parts) != 2 or parts[0].lower() != "bearer":
            raise AuthenticationFailed(
                "Invalid authorization header."
            )

        token = parts[1]

        try:
            payload = jwt.decode(
                token,
                settings.SECRET_KEY,
                algorithms=[settings.JWT_ALGORITHM],
            )

        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed(
                "Token has expired."
            )

        except jwt.InvalidTokenError:
            raise AuthenticationFailed(
                "Invalid token."
            )

        if payload.get("type") != "access":
            raise AuthenticationFailed(
                "Invalid token type."
            )

        user_id = payload.get("sub")

        if not user_id:
            raise AuthenticationFailed(
                "Invalid token."
            )

        try:
            user = UserModel.objects.get(id=user_id)

        except UserModel.DoesNotExist:
            raise AuthenticationFailed(
                "User not found."
            )

        return (user, token)
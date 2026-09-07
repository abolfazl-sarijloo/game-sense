from src.application.use_cases.login_user import LoginUserUseCase
from src.application.use_cases.register_user import RegisterUserUseCase

from src.infrastructure.persistence.django.repositories.user_repository import (
    DjangoUserRepository,
)

from src.infrastructure.security.jwt_token_generator import (
    JWTTokenGenerator,
)

from src.infrastructure.security.password_hasher import (
    DjangoPasswordHasher,
)


class Container:

    @staticmethod
    def register_user_use_case() -> RegisterUserUseCase:
        return RegisterUserUseCase(
            user_repository=DjangoUserRepository(),
            password_hasher=DjangoPasswordHasher(),
        )

    @staticmethod
    def login_user_use_case() -> LoginUserUseCase:
        return LoginUserUseCase(
            user_repository=DjangoUserRepository(),
            password_hasher=DjangoPasswordHasher(),
            token_generator=JWTTokenGenerator(),
        )
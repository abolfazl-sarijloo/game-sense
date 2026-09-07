import pytest

from src.application.dto.register_user import RegisterUserDTO
from src.application.use_cases.register_user import RegisterUserUseCase


class FakeUserRepository:

    def __init__(self):
        self.users = []

    def exists_by_email(self, email: str) -> bool:
        return any(
            user.email == email
            for user in self.users
        )

    def create(self, user):
        self.users.append(user)
        return user


class FakePasswordHasher:

    def hash(self, password: str) -> str:
        return f"hashed:{password}"

    def verify(self, password: str, password_hash: str) -> bool:
        return password_hash == f"hashed:{password}"


def test_register_user():
    repository = FakeUserRepository()
    password_hasher = FakePasswordHasher()

    use_case = RegisterUserUseCase(
        user_repository=repository,
        password_hasher=password_hasher,
    )

    dto = RegisterUserDTO(
        username="abolfazl",
        email="abolfazl@example.com",
        password="12345678",
    )

    user = use_case.execute(dto)

    assert user.username == "abolfazl"
    assert user.email == "abolfazl@example.com"
    assert user.password_hash == "hashed:12345678"


def test_register_user_with_existing_email():
    repository = FakeUserRepository()
    password_hasher = FakePasswordHasher()

    use_case = RegisterUserUseCase(
        user_repository=repository,
        password_hasher=password_hasher,
    )

    dto = RegisterUserDTO(
        username="abolfazl",
        email="abolfazl@example.com",
        password="12345678",
    )

    use_case.execute(dto)

    with pytest.raises(
        ValueError,
        match="User with this email already exists.",
    ):
        use_case.execute(dto)
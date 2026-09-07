from src.application.dto.register_user import RegisterUserDTO
from src.domain.entities.user import User
from src.domain.repositories.password_hasher import PasswordHasher
from src.domain.repositories.user_repository import UserRepository


class RegisterUserUseCase:

    def __init__(
        self,
        user_repository: UserRepository,
        password_hasher: PasswordHasher,
    ):
        self._user_repository = user_repository
        self._password_hasher = password_hasher

    def execute(self, data: RegisterUserDTO) -> User:

        if self._user_repository.exists_by_email(data.email):
            raise ValueError(
                "User with this email already exists."
            )

        password_hash = self._password_hasher.hash(
            data.password
        )

        user = User.create(
            username=data.username,
            email=data.email,
            password_hash=password_hash,
        )

        return self._user_repository.create(user)
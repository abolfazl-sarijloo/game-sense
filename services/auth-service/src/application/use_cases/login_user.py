from src.application.dto.login_result import LoginResult
from src.application.dto.login_user import LoginUserDTO
from src.domain.repositories.password_hasher import PasswordHasher
from src.domain.repositories.token_generator import TokenGenerator
from src.domain.repositories.user_repository import UserRepository


class LoginUserUseCase:

    def __init__(
        self,
        user_repository: UserRepository,
        password_hasher: PasswordHasher,
        token_generator: TokenGenerator,
    ):
        self._user_repository = user_repository
        self._password_hasher = password_hasher
        self._token_generator = token_generator

    def execute(self, data: LoginUserDTO) -> LoginResult:

        user = self._user_repository.get_by_email(data.email)

        if user is None:
            raise ValueError("Invalid email or password.")

        password_valid = self._password_hasher.verify(
            data.password,
            user.password_hash,
        )

        if not password_valid:
            raise ValueError("Invalid email or password.")

        access_token = self._token_generator.generate_access_token(user)

        return LoginResult(
            access_token=access_token,
        )
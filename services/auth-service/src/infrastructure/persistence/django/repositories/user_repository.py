from typing import Optional
from uuid import UUID

from src.domain.entities.user import User
from src.domain.repositories.user_repository import UserRepository
from src.presentation.users.models import UserModel


class DjangoUserRepository(UserRepository):

    def create(self, user: User) -> User:
        user_model = UserModel.objects.create(
            id=user.id,
            username=user.username,
            email=user.email,
            password_hash=user.password_hash,
        )

        return self._to_domain(user_model)

    def get_by_id(self, user_id: UUID) -> Optional[User]:
        try:
            user_model = UserModel.objects.get(id=user_id)
        except UserModel.DoesNotExist:
            return None

        return self._to_domain(user_model)

    def get_by_email(self, email: str) -> Optional[User]:
        try:
            user_model = UserModel.objects.get(email=email)
        except UserModel.DoesNotExist:
            return None

        return self._to_domain(user_model)

    def exists_by_email(self, email: str) -> bool:
        return UserModel.objects.filter(email=email).exists()

    @staticmethod
    def _to_domain(user_model: UserModel) -> User:
        return User(
            id=user_model.id,
            username=user_model.username,
            email=user_model.email,
            password_hash=user_model.password_hash,
            created_at=user_model.created_at,
            updated_at=user_model.updated_at,
        )
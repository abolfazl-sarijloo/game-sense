from django.contrib.auth.hashers import check_password, make_password

from src.domain.repositories.password_hasher import PasswordHasher


class DjangoPasswordHasher(PasswordHasher):

    def hash(self, password: str) -> str:
        return make_password(password)

    def verify(self, password: str, password_hash: str) -> bool:
        return check_password(password, password_hash)
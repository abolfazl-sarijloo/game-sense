from dataclasses import dataclass


@dataclass(frozen=True)
class RegisterUserDTO:
    username: str
    email: str
    password: str
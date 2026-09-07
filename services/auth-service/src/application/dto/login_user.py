from dataclasses import dataclass


@dataclass(frozen=True)
class LoginUserDTO:
    email: str
    password: str
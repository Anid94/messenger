from exceptions import EmailAlreadyRegistered, InvalidCredentials
from models import UsersTable
from repo.users import UsersRepo
from security import hash_password, verify_password, create_access_token


class UserService:
    def __init__(self, repo: UsersRepo):
        self.repo = repo

    def register(self, email: str, password: str) -> UsersTable:
        if self.repo.get_by_email(email) is not None:
            raise EmailAlreadyRegistered
        user = self.repo.create(email, hash_password(password))
        if user is None:
            raise EmailAlreadyRegistered
        return user

    def authenticate(self, email: str, password: str) -> str:
        user = self.repo.get_by_email(email)
        if user is None or not verify_password(password, user.password_hash):
            raise InvalidCredentials
        return create_access_token(user.id)

    def list_users(self, limit: int = 100, offset: int = 0) -> list[UsersTable]:
        return self.repo.list(limit=limit, offset=offset)
from exceptions import EmailAlreadyRegistered, InvalidCredentials, UsernameTaken
from models import UsersTable
from repo.users import UsersRepo
from security import hash_password, verify_password, create_access_token


class UserService:
    def __init__(self, repo: UsersRepo):
        self.repo = repo

    def register(self, email: str, username: str, display_name: str, password: str) -> UsersTable:
        if self.repo.get_by_email(email) is not None:
            raise EmailAlreadyRegistered
        if self.repo.get_by_username(username) is not None:
            raise UsernameTaken
        user = self.repo.create(email=email, username=username, display_name=display_name, password_hash=hash_password(password))
        if user is None:
            if self.repo.get_by_email(email) is not None:
                raise EmailAlreadyRegistered
            raise UsernameTaken
        return user

    def search_users(self, current_user_id: int, query: str, limit: int = 20) -> list[UsersTable]:
        query = query.strip().lower()
        if not query:
            return []
        return self.repo.search_by_username(query, current_user_id, limit)

    def update_profile(self, user: UsersTable, username: str | None, display_name: str | None) -> UsersTable:
        if username is not None and username != user.username:
            if self.repo.get_by_username(username) is not None:
                raise UsernameTaken
        updated = self.repo.update_profile(user, username, display_name)
        if updated is None:
            raise UsernameTaken
        return updated

    def authenticate(self, email: str, password: str) -> str:
        user = self.repo.get_by_email(email)
        if user is None or not verify_password(password, user.password_hash):
            raise InvalidCredentials
        return create_access_token(user.id)

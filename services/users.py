import models
from repo.users import UsersRepo
from schemas import Registration
from security import hash_password, verify_password, create_access_token


class UserService:
    def __init__(self, repo: UsersRepo):
        self.repo = repo

    def register(self, email, password) -> Registration:
        user = self.repo.get_by_email(email)
        if user is None:
            return self.repo.registration(email, hash_password(password))
        return None

    def auth(self, email: str, password: str):
        user = self.repo.get_by_email(email)
        if user is None or not verify_password(password, user.password_hash):
            return None
        return {
            "access_token": create_access_token(user.id),
            "token_type": "bearer",
        }

    def get_user_list(self):
        return self.repo.list()
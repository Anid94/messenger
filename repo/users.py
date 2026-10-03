from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from models import UsersTable


class UsersRepo:
    def __init__(self, db: Session):
        self.db = db

    def get_by_email(self, email: str) -> UsersTable | None:
        return self.db.scalar(
            select(UsersTable).where(UsersTable.email == email)
        )

    def get_by_id(self, user_id) -> UsersTable | None:
        return self.db.get(UsersTable, user_id)

    def get_by_username(self, username: str) -> UsersTable | None:
        return self.db.scalar(select(UsersTable).where(UsersTable.username == username))

    def list(self, limit: int = 100, offset: int = 0) -> list[UsersTable]:
        result = select(UsersTable).order_by(UsersTable.id).limit(limit).offset(offset)
        return list(self.db.scalars(result))

    def create(self, email: str, username: str, display_name: str, password_hash: str) -> UsersTable | None:
        user = UsersTable(email=email, username=username, display_name=display_name, password_hash=password_hash)
        self.db.add(user)
        try:
            self.db.commit()
        except IntegrityError:
            self.db.rollback()
            return None
        self.db.refresh(user)
        return user

    def update_profile(self, user: UsersTable, username: str | None, display_name: str | None) -> UsersTable | None:
        if username is not None:
            user.username = username
        if display_name is not None:
            user.display_name = display_name
        try:
            self.db.commit()
        except IntegrityError:
            self.db.rollback()
            return None
        self.db.refresh(user)
        return user
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

    def list(self, limit: int = 100, offset: int = 0) -> list[UsersTable]:
        result = select(UsersTable).order_by(UsersTable.id).limit(limit).offset(offset)
        return list(self.db.scalars(result))

    def create(self, email: str, password_hash: str) -> UsersTable | None:
        user = UsersTable(email=email, password_hash=password_hash)
        self.db.add(user)
        try:
            self.db.commit()
        except IntegrityError:
            self.db.rollback()
            return None
        self.db.refresh(user)
        return user
from sqlalchemy import select
from sqlalchemy.orm import Session

from schemas import UserRead
from models import UsersTable


class UsersRepo:
    def __init__(self, db: Session):
        self.db = db

    def get_by_email(self, email) -> UsersTable | None:
        stmt = select(UsersTable).where(UsersTable.email == email)
        return self.db.scalar(stmt)

    def get_by_id(self, user_id) -> UsersTable | None:
        return self.db.get(UsersTable, user_id)

    def list(self):
        return self.db.query(UsersTable).all()

    def registration(self, email, hash_password) -> UsersTable:
        user = UsersTable(email=email, password_hash=hash_password)
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)
        return user


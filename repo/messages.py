from sqlalchemy import select, or_, and_
from sqlalchemy.orm import Session

from models import MessagesTable


class MessagesRepo:
    def __init__(self, db: Session):
        self.db = db

    def create(self, sender_id: int, recipient_id: int, text: str) -> MessagesTable:
        message = MessagesTable(
            sender_id=sender_id,
            recipient_id=recipient_id,
            text=text,
        )
        self.db.add(message)
        self.db.commit()
        self.db.refresh(message)
        return message

    def get_dialog(self, user_a: int, user_b: int, limit: int = 50, before_id: int | None = None) -> list[MessagesTable]:
        pair = or_(
            and_(
                MessagesTable.sender_id == user_a,
                MessagesTable.recipient_id == user_b,
            ),
            and_(
                MessagesTable.sender_id == user_b,
                MessagesTable.recipient_id == user_a,
            ),
        )
        stmt = select(MessagesTable).where(pair)
        if before_id is not None:
            stmt = stmt.where(MessagesTable.id < before_id)

        # последние limit сообщений
        stmt = stmt.order_by(MessagesTable.id.desc()).limit(limit)
        rows = list(self.db.scalars(stmt))
        rows.reverse()
        return rows
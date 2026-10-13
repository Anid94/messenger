from sqlalchemy import select, or_, and_
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from models import ContactsTable, UsersTable


class ContactsRepo:
    def __init__(self, db: Session):
        self.db = db

    def get_pair(
            self,
            user_a: int,
            user_b: int,
    ) -> ContactsTable | None:
        pair = or_(
            and_(
                ContactsTable.requester_id == user_a,
                ContactsTable.addressee_id == user_b,
            ),
            and_(
                ContactsTable.requester_id == user_b,
                ContactsTable.addressee_id == user_a,
            ),
        )
        return self.db.scalar(select(ContactsTable).where(pair))

    def create(
            self,
            requester_id: int,
            addressee_id: int,
    ) -> ContactsTable | None:
        contact = ContactsTable(
            requester_id=requester_id,
            addressee_id=addressee_id,
            status="pending"
        )
        self.db.add(contact)
        try:
            self.db.commit()
        except IntegrityError:
            self.db.rollback()
            return None
        self.db.refresh(contact)
        return contact

    def list_incoming(
            self,
            user: UsersTable,
            contact: ContactsTable,
    ) -> list[ContactsTable] | None:
        stmt = (
            select(contact, user).join(user, contact.requester_id == user.id)
            .where(contact.status == "pending")
        )

        return self.db.scalars(stmt).all()

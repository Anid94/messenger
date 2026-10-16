from datetime import datetime

from sqlalchemy import select, or_, and_, exists
from sqlalchemy.orm import Session

from models import ContactsTable


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

    def get_by_id(self, contact_id: int) -> ContactsTable:
        return self.db.get(ContactsTable, contact_id)

    def create(self, requester_id: int, addressee_id: int) -> ContactsTable:
        contact = ContactsTable(
            requester_id=requester_id,
            addressee_id=addressee_id,
            status="pending",
        )
        self.db.add(contact)
        return contact

    def list_incoming(self, user_id: int) -> list[ContactsTable]:
        stmt = (
            select(ContactsTable)
            .where(ContactsTable.addressee_id == user_id)
            .where(ContactsTable.status == "pending")
        )
        return list(self.db.scalars(stmt))

    def list_contacts(self, user_id: int) -> list[ContactsTable]:
        stmt = select(ContactsTable).where(
            or_(
                ContactsTable.requester_id == user_id,
                ContactsTable.addressee_id == user_id,
            )
        ).where(ContactsTable.status == "accepted")
        return list(self.db.scalars(stmt))

    def accept(self, contact: ContactsTable) -> ContactsTable:
        contact.status = "accepted"
        contact.responded_at = datetime.now()
        return contact

    def decline(self, contact: ContactsTable) -> None:
        self.db.delete(contact)

    def delete(self, contact: ContactsTable) -> None:
        self.db.delete(contact)

    def has_accepted(self, my_id: int, user_id: int) -> bool:
        pair = or_(
            and_(
                ContactsTable.requester_id == my_id,
                ContactsTable.addressee_id == user_id,
            ),
            and_(
                ContactsTable.requester_id == user_id,
                ContactsTable.addressee_id == my_id,
            ),
        )
        stmt = (
            select(ContactsTable)
            .where(pair)
            .where(ContactsTable.status == "accepted")
        )
        return self.db.scalar(select(exists(stmt)))
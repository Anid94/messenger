from repo.contacts import ContactsRepo
from models import ContactsTable
from exceptions import ContactAlreadyExists, CannotAddSelf, ContactRequestNotFound
from sqlalchemy.exc import IntegrityError


class ContactService:
    def __init__(self, repo: ContactsRepo):
        self.repo = repo

    def send_request(self, requester_id: int, addressee_id: int) -> ContactsTable:
        if requester_id == addressee_id:
            raise CannotAddSelf
        if self.repo.get_pair(requester_id, addressee_id) is not None:
            raise ContactAlreadyExists
        contact = self.repo.create(requester_id, addressee_id)
        try:
            self.repo.db.commit()
            self.repo.db.refresh(contact)
            return contact
        except IntegrityError:
            self.repo.db.rollback()
            raise ContactAlreadyExists

    def list_incoming(self, user_id: int) -> list[ContactsTable]:
        return self.repo.list_incoming(user_id)

    def list_contacts(self, user_id: int) -> list[ContactsTable]:
        return self.repo.list_contacts(user_id)

    def accept(self, contact_id: int, user_id: int) -> ContactsTable:
        contact = self.repo.get_by_id(contact_id)
        if contact is None or contact.addressee_id != user_id:
            raise ContactRequestNotFound
        self.repo.accept(contact)
        self.repo.db.commit()
        self.repo.db.refresh(contact)
        return contact

    def decline(self, contact_id: int, user_id: int) -> None:
        contact = self.repo.get_by_id(contact_id)
        if contact is None or contact.addressee_id != user_id:
            raise ContactRequestNotFound
        self.repo.decline(contact)
        self.repo.db.commit()

    def remove(self, contact_id: int, user_id: int) -> None:
        contact = self.repo.get_by_id(contact_id)
        if contact is None:
            raise ContactRequestNotFound
        if user_id not in(contact.requester_id, contact.addressee_id):
            raise ContactRequestNotFound
        self.repo.delete(contact)
        self.repo.db.commit()
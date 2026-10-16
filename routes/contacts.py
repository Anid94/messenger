from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from database import get_db
from models import ContactsTable, UsersTable
from repo.contacts import ContactsRepo
from routes.dependencies import get_current_user
from services.contacts import ContactService
from schemas import ContactRead, ContactCreate


router = APIRouter(prefix="/app/contacts", tags=["contacts"])

def get_contact_service(db: Session = Depends(get_db)) -> ContactService:
    return ContactService(ContactsRepo(db))




@router.get("/incoming", response_model=list[ContactRead])
def list_incoming(
        current_user: UsersTable = Depends(get_current_user),
        service: ContactService = Depends(get_contact_service),
):
    return service.list_incoming(current_user.id)


@router.get("", response_model=list[ContactRead])
def list_contacts(
        current_user: UsersTable = Depends(get_current_user),
        service: ContactService = Depends(get_contact_service)
):
    return service.list_contacts(current_user.id)


@router.post(
    "",
    response_model=ContactRead,
    status_code=201,
    responses={
        400: {"description": "Cannot add yourself"},
        409: {"description": "Contact already exists"},
    },
)
def send_request(
        contact: ContactCreate,
        current_user: UsersTable = Depends(get_current_user),
        service: ContactService = Depends(get_contact_service),
):
    return service.send_request(
        requester_id=current_user.id,
        addressee_id=contact.addressee_id,
    )


@router.post(
    "/{contact_id}/accept",
    response_model=ContactRead,
    responses={404: {"description": "Contact not found"}},
)
def accept(
        contact_id: int,
        current_user: UsersTable = Depends(get_current_user),
        service: ContactService = Depends(get_contact_service),
):
    return service.accept(contact_id, current_user.id)


@router.post(
    "/{contact_id}/decline",
    responses={404: {"description": "Contact not found"}},
)
def decline(
        contact_id: int,
        current_user: UsersTable = Depends(get_current_user),
        service: ContactService = Depends(get_contact_service),
):
    return service.decline(contact_id, current_user.id)


@router.delete(
    "/{contact_id}",
    responses={404: {"description": "Contact not found"}},
)
def remove(
        contact_id: int,
        current_user: UsersTable = Depends(get_current_user),
        service: ContactService = Depends(get_contact_service),
):
    return service.remove(contact_id, current_user.id)
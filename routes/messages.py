from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database import get_db
from routes.dependencies import get_current_user
from models import UsersTable
from repo.messages import MessagesRepo
from repo.users import UsersRepo
from services.messages import MessageService
from schemas import MessageCreate, MessageRead

router = APIRouter(prefix="/app/messages", tags=["messages"])


def get_message_service(db: Session = Depends(get_db)) -> MessageService:
    return MessageService(MessagesRepo(db), UsersRepo(db))

@router.post("", response_model=MessageRead, status_code=201)
def send_message(
        payload: MessageCreate,
        current_user: UsersTable = Depends(get_current_user),
        service: MessageService = Depends(get_message_service),
):
    message, error = service.send(
        sender_id=current_user.id,
        recipient_id=payload.recipient_id,
        text=payload.text,
    )
    if error == "recipient_not_found":
        raise HTTPException(status_code=404, detail="Recipient not found")
    if error == "cannot_send_to_self":
        raise HTTPException(status_code=400, detail="Cannot send message to yourself")
    return message


@router.get("/dialog/{other_user_id}", response_model=list[MessageRead])
def get_dialog(
        other_user_id: int,
        current_user: UsersTable = Depends(get_current_user),
        service: MessageService = Depends(get_message_service),
):
    return service.dialog(current_user.id, other_user_id)
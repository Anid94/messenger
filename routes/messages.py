from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from database import get_db
from models import UsersTable
from repo.messages import MessagesRepo
from repo.users import UsersRepo
from routes.dependencies import get_current_user
from schemas import MessageCreate, MessageRead
from services.messages import MessageService

router = APIRouter(prefix="/app/messages", tags=["messages"])


def get_message_service(db: Session = Depends(get_db)) -> MessageService:
    return MessageService(MessagesRepo(db), UsersRepo(db))

@router.post(
    "",
    response_model=MessageRead,
    status_code=201,
    responses={
        400: {"description": "Cannot send message to yourself"},
        404: {"description": "Recipient not found"},
    },
)
def send_message(
        payload: MessageCreate,
        current_user: UsersTable = Depends(get_current_user),
        service: MessageService = Depends(get_message_service),
):
    return service.send(
        sender_id=current_user.id,
        recipient_id=payload.recipient_id,
        text=payload.text,
    )


@router.get(
    "/dialog/{other_user_id}",
    response_model=list[MessageRead],
    responses={404: {"description": "User not found"}},
)
def get_dialog(
        other_user_id: int,
        limit: int = Query(50, ge=1, le=200),
        before_id: int | None = Query(None, gt=0),
        current_user: UsersTable = Depends(get_current_user),
        service: MessageService = Depends(get_message_service),
):
    return service.dialog(
        current_user.id, other_user_id, limit=limit, before_id=before_id
    )
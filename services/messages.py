from exceptions import CannotMessageSelf, UserNotFound
from models import MessagesTable
from repo.messages import MessagesRepo
from repo.users import UsersRepo


class MessageService:
    def __init__(self, messages_repo: MessagesRepo, users_repo: UsersRepo):
        self.messages_repo = messages_repo
        self.users_repo = users_repo

    def send(self, sender_id: int, recipient_id: int, text: str) -> MessagesTable:
        if sender_id == recipient_id:
            raise CannotMessageSelf
        if self.users_repo.get_by_id(recipient_id) is None:
            raise UserNotFound
        return self.messages_repo.create(sender_id, recipient_id, text)

    def dialog(self, user_a: int, user_b: int, limit: int = 50, before_id: int | None = None) -> list[MessagesTable]:
        if self.users_repo.get_by_id(user_b) is None:
            raise UserNotFound
        return self.messages_repo.get_dialog(
            user_a, user_b, limit=limit, before_id=before_id
        )
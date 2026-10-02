from repo.messages import MessagesRepo
from repo.users import UsersRepo


class MessageService:
    def __init__(self, messages_repo: MessagesRepo, users_repo: UsersRepo):
        self.messages_repo = messages_repo
        self.users_repo = users_repo

    def send(self, sender_id: int, recipient_id: int, text: str):
        if sender_id == recipient_id:
            return None, "cannot_send_to_self"
        recipient = self.users_repo.get_by_id(recipient_id)
        if recipient is None:
            return None, "recipient_not_found"
        message = self.messages_repo.create(sender_id, recipient_id, text)
        return message, None

    def dialog(self, user_a: int, user_b: int):
        return self.messages_repo.get_dialog(user_a, user_b)
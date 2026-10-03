class AppError(Exception):
    """Нарушение бизнес-правила. Превращается в HTTP-ответ одним обработчиком."""

    status_code: int = 400
    detail: str = "Request cannot be processed"


class EmailAlreadyRegistered(AppError):
    status_code: int = 409
    detail: str = "Email already registered"


class InvalidCredentials(AppError):
    status_code: int = 401
    detail: str = "Invalid email or password"


class InvalidToken(AppError):
    status_code: int = 401
    detail: str = "Invalid or expired token"


class UserNotFound(AppError):
    status_code: int = 404
    detail: str = "User not found"


class CannotMessageSelf(AppError):
    status_code: int = 400
    detail: str = "Cannot send message to yourself"
class AppError(Exception):
    """Нарушение бизнес-правила. Превращается в HTTP-ответ одним обработчиком."""

    status_code = 400
    detail = "Request cannot be processed"


class EmailAlreadyRegistered(AppError):
    status_code = 409
    detail = "Email already registered"


class InvalidCredentials(AppError):
    status_code = 401
    detail = "Invalid email or password"


class InvalidToken(AppError):
    status_code = 401
    detail = "Invalid or expired token"


class UserNotFound(AppError):
    status_code = 404
    detail = "User not found"


class CannotMessageSelf(AppError):
    status_code = 400
    detail = "Cannot send message to yourself"
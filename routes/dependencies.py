from fastapi import Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session

from database import get_db
from exceptions import InvalidToken
from models import UsersTable
from security import decode_access_token
from repo.users import UsersRepo

bearer_scheme = HTTPBearer()


def get_current_user(
        credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
        db: Session = Depends(get_db),
) -> UsersTable:
    user_id = decode_access_token(credentials.credentials)
    user = UsersRepo(db).get_by_id(user_id)
    if user is None:
        raise InvalidToken
    return user
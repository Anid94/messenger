from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from database import get_db
from models import UsersTable
from repo.users import UsersRepo
from routes.dependencies import get_current_user
from schemas import UserRead, Registration, Authenticate, TokenOut
from services.users import UserService


router = APIRouter(prefix="/app/users", tags=["users"])

def get_user_service(db: Session = Depends(get_db)) -> UserService:
    return UserService(UsersRepo(db))


@router.get("", response_model=list[UserRead])
def get_users(
        limit: int = Query(100, ge=1, le=200),
        offset: int = Query(0, ge=0),
        _: UserService = Depends(get_user_service),
        service: UserService = Depends(get_user_service),
):
    return service.list_users(limit=limit, offset=offset)

#для фронтенд
@router.get("/me", response_model=UserRead)
def get_me(current_user: UsersTable = Depends(get_current_user)):
    return current_user

@router.post(
    "/reg",
    response_model=UserRead,
    status_code=201,
    responses={409: {"description": "Email already registered"}},
)
def register(payload: Registration, service: UserService = Depends(get_user_service)):
    return service.register(payload.email, payload.password)

@router.post(
    "/auth",
    response_model=TokenOut,
    responses={401: {"description": "Invalid email or password"}},
)
def login(credentials: Authenticate, service: UserService = Depends(get_user_service)):
    token = service.authenticate(credentials.email, credentials.password)
    return TokenOut(access_token=token)
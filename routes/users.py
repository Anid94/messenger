from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from database import get_db
from models import UsersTable
from repo.users import UsersRepo
from routes.dependencies import get_current_user
from schemas import Authenticate, ProfileUpdate, Registration, TokenOut, UserMe, UserPublic
from services.users import UserService


router = APIRouter(prefix="/app/users", tags=["users"])

def get_user_service(db: Session = Depends(get_db)) -> UserService:
    return UserService(UsersRepo(db))


@router.get("", response_model=list[UserPublic])
def get_users(
        limit: int = Query(100, ge=1, le=200),
        offset: int = Query(0, ge=0),
        _: UsersTable = Depends(get_current_user),
        service: UserService = Depends(get_user_service),
):
    return service.list_users(limit=limit, offset=offset)


#для фронтенд
@router.get("/me", response_model=UserMe)
def get_me(current_user: UsersTable = Depends(get_current_user)):
    return current_user


@router.patch(
    "/me",
    response_model=UserMe,
    responses={409: {"description": "Username already taken"}},
)
def update_me(
        payload: ProfileUpdate,
        current_user: UsersTable = Depends(get_current_user),
        service: UserService = Depends(get_user_service),
):
    return service.update_profile(current_user, payload.username, payload.display_name)


@router.get("/search", response_model=list[UserPublic])
def search_users(
        query: str = Query(..., min_length=1, max_length=32),
        limit: int = Query(20, ge=1, le=50),
        current_user: UsersTable = Depends(get_current_user),
        service: UserService = Depends(get_user_service),
):
    return service.search_users(current_user.id, query, limit)


@router.post(
    "/reg",
    response_model=UserMe,
    status_code=201,
    responses={409: {"description": "Email already registered"}},
)
def register(payload: Registration, service: UserService = Depends(get_user_service)):
    return service.register(
        email=payload.email,
        username=payload.username,
        display_name=payload.display_name,
        password=payload.password,
    )

@router.post(
    "/auth",
    response_model=TokenOut,
    responses={401: {"description": "Invalid email or password"}},
)
def login(credentials: Authenticate, service: UserService = Depends(get_user_service)):
    token = service.authenticate(credentials.email, credentials.password)
    return TokenOut(access_token=token)
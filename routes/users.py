from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database import get_db
from repo.users import UsersRepo
from services.users import UserService
from schemas import UserRead, Registration, Authenticate, TokenOut

from routes.dependencies import get_current_user
from models import UsersTable

router = APIRouter(prefix="/app/users", tags=["users"])

def get_user_repo(db: Session = Depends(get_db)) -> UsersRepo:
    return UsersRepo(db)

def get_user_service(repo: UsersRepo = Depends(get_user_repo)) -> UserService:
    return UserService(repo)


@router.get("", response_model=list[UserRead])
def get_users(service: UserService = Depends(get_user_service)):
    return service.get_user_list()

#для фронтенд
@router.get("/me", response_model=UserRead)
def get_me(current_user: UsersTable = Depends(get_current_user)):
    return current_user

@router.post("/reg", response_model=UserRead, status_code=201)
def register(payload: Registration, service: UserService = Depends(get_user_service)):
    result = service.register(payload.email, payload.password)
    if result is None:
        raise HTTPException(status_code=409, detail="Email already registered")
    return result

@router.post("/auth", response_model=TokenOut, status_code=200)
def login(credentials: Authenticate, service: UserService = Depends(get_user_service)):
    result = service.auth(credentials.email, credentials.password)
    if result is None:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    return result
from pydantic import BaseModel, EmailStr, ConfigDict
from datetime import datetime

class Registration(BaseModel):
    email: EmailStr
    password: str


class UserRead(BaseModel):
    id: int
    email: str

    model_config = ConfigDict(from_attributes=True)


class Authenticate(BaseModel):
    email: EmailStr
    password: str


class TokenOut(BaseModel):
    access_token: str
    token_type: str = "bearer"


class MessageCreate(BaseModel):
    recipient_id: int
    text: str


class MessageRead(BaseModel):
    id: int
    sender_id: int
    recipient_id: int
    text: str
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
from datetime import datetime

from pydantic import BaseModel, EmailStr, Field, ConfigDict, field_validator


class EmailIn(BaseModel):
    email: EmailStr = Field(max_length=255)

    @field_validator("email")
    @classmethod
    def normalize_email(cls, value: str) -> str:
        return value.strip().lower()


class Registration(EmailIn):
    password: str = Field(min_length=8, max_length=128)


class Authenticate(EmailIn):
    password: str = Field(min_length=1, max_length=128)


class UserRead(BaseModel):
    id: int
    email: EmailStr

    model_config = ConfigDict(from_attributes=True)


class TokenOut(BaseModel):
    access_token: str
    token_type: str = "bearer"


class MessageCreate(BaseModel):
    recipient_id: int = Field(gt=0)
    text: str = Field(min_length=1, max_length=4000)

    @field_validator("text")
    @classmethod
    def strip_text(cls, value: str) -> str:
        cleaned = value.strip()
        if not cleaned:
            raise ValueError("Message text cannot be empty")
        return cleaned


class MessageRead(BaseModel):
    id: int
    sender_id: int
    recipient_id: int
    text: str
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
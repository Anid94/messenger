import re
from datetime import datetime

from pydantic import BaseModel, EmailStr, Field, ConfigDict, field_validator


USERNAME_RE = re.compile(r"^[a-z][a-z0-9_]{2,31}$")

def clean_username(value: str) -> str:
    value = value.strip().lower()
    if not USERNAME_RE.fullmatch(value):
        raise ValueError("Username must start with a letter and contain only latin letters, digits and underscore")
    return value

def clean_display_name(value: str) -> str:
    cleaned = " ".join(value.split())
    if not cleaned:
        raise ValueError("Display name cannot be empty")
    return cleaned


class EmailIn(BaseModel):
    email: EmailStr = Field(max_length=255)

    @field_validator("email")
    @classmethod
    def normalize_email(cls, value: str) -> str:
        return value.strip().lower()


class Registration(EmailIn):
    username: str = Field(min_length=3, max_length=32)
    display_name: str = Field(min_length=1, max_length=64)
    password: str = Field(min_length=8, max_length=128)

    _normal_username = field_validator("username")(classmethod(lambda cls, v: clean_username(v)))
    _normal_display = field_validator("display_name")(classmethod(lambda cls, v: clean_display_name(v)))


class Authenticate(EmailIn):
    password: str = Field(min_length=1, max_length=128)


class ProfileUpdate(BaseModel):
    username: str | None = Field(None, min_length=3, max_length=32)
    display_name: str | None = Field(None, min_length=1, max_length=64)

    model_config = ConfigDict(extra="forbid")

    @field_validator("username")
    @classmethod
    def normal_username(cls, value: str | None) -> str | None:
        return None if value is None else clean_username(value)

    @field_validator("display_name")
    @classmethod
    def normal_display_name(cls, value: str | None) -> str | None:
        return None if value is None else clean_display_name(value)


class UserPublic(BaseModel):
    id: int
    username: str
    display_name: str

    model_config = ConfigDict(from_attributes=True)


class UserMe(UserPublic):
    email: EmailStr
    created_at: datetime


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
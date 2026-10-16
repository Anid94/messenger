from datetime import datetime

from sqlalchemy import (
    DateTime,
    ForeignKey,
    Index,
    Integer,
    String,
    Text,
    UniqueConstraint,
    func,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database import Base


class UsersTable(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    email: Mapped[str] = mapped_column(String(255), nullable=False, unique=True)
    username: Mapped[str] = mapped_column(String(32), nullable=False)
    display_name: Mapped[str] = mapped_column(String(64), nullable=False)
    password_hash: Mapped[str] = mapped_column(String(255), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, server_default=func.now())

    sent_contacts = relationship(
        "ContactsTable",
        foreign_keys="ContactsTable.requester_id",
        back_populates="requester",
        cascade="all",
        passive_deletes=True,
    )
    received_contacts = relationship(
        "ContactsTable",
        foreign_keys="ContactsTable.addressee_id",
        back_populates="addressee",
        cascade="all",
        passive_deletes=True,
    )

    __table_args__ = (
        UniqueConstraint("username", name="uq_users_username"),
    )


class MessagesTable(Base):
    __tablename__ = "messages"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    sender_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    recipient_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    text: Mapped[str] = mapped_column(Text, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, server_default=func.now())

    __table_args__ = (
        Index("ix_messages_sender_recipient_created", "sender_id", "recipient_id", "created_at"),
        Index("ix_messages_recipient_sender_created", "recipient_id", "sender_id", "created_at"),
    )


class ContactsTable(Base):
    __tablename__ = "contacts"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    requester_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    addressee_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    status: Mapped[str] = mapped_column(String(14), default="pending")
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, server_default=func.now())
    responded_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)

    requester = relationship(
        "UsersTable",
        foreign_keys=[requester_id],
        back_populates="sent_contacts",
    )
    addressee = relationship(
        "UsersTable",
        foreign_keys=[addressee_id],
        back_populates="received_contacts",
    )

    __table_args__ = (
        UniqueConstraint("requester_id", "addressee_id", name="uq_requester_addressee_pair"),
        Index("ix_contacts_addressee", "addressee_id")
    )


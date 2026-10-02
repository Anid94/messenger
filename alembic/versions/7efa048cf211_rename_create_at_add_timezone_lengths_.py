"""rename create_at, add_timezone, lengths and indexes

Revision ID: 7efa048cf211
Revises: b11b017d846f
Create Date: 2026-10-02 12:34:14.479759

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '7efa048cf211'
down_revision: Union[str, Sequence[str], None] = 'b11b017d846f'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.alter_column("users", "create_at", new_column_name="created_at")

    op.execute("UPDATE users SET email = lower(email)")

    op.alter_column(
        "users",
        "created_at",
        existing_type=sa.DateTime(),
        type_=sa.DateTime(timezone=True),
        existing_nullable=False,
        existing_server_default=sa.text("now()"),
        postgresql_using="created_at AT TIME ZONE 'UTC'",
    )
    op.alter_column(
        "users",
        "email",
        existing_type=sa.String(),
        type_=sa.String(length=255),
        existing_nullable=False,
    )
    op.alter_column(
        "users",
        "password_hash",
        existing_type=sa.String(),
        type_=sa.String(length=255),
        existing_nullable=False,
    )

    op.alter_column(
        "messages",
        "created_at",
        existing_type=sa.DateTime(),
        type_=sa.DateTime(timezone=True),
        existing_nullable=False,
        existing_server_default=sa.text("now()"),
        postgresql_using="created_at AT TIME ZONE 'UTC'",
    )
    op.alter_column(
        "messages",
        "text",
        existing_type=sa.String(),
        type_=sa.Text(),
        existing_nullable=False,
    )

    op.create_index(
        "ix_messages_sender_recipient_created",
        "messages",
        ["sender_id", "recipient_id", "created_at"],
    )
    op.create_index(
        "ix_messages_recipient_sender_created",
        "messages",
        ["recipient_id", "sender_id", "created_at"],
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_index("ix_messages_recipient_sender_created", table_name="messages")
    op.drop_index("ix_messages_sender_recipient_created", table_name="messages")

    op.alter_column(
        "messages",
        "text",
        existing_type=sa.Text(),
        type_=sa.String(),
        existing_nullable=False,
    )
    op.alter_column(
        "messages",
        "created_at",
        existing_type=sa.DateTime(timezone=True),
        type_=sa.DateTime(),
        existing_nullable=False,
        existing_server_default=sa.text("now()"),
    )
    op.alter_column(
        "users",
        "password_hash",
        existing_type=sa.String(length=255),
        type_=sa.String(),
        existing_nullable=False,
    )
    op.alter_column(
        "users",
        "email",
        existing_type=sa.String(length=255),
        type_=sa.String(),
        existing_nullable=False,
    )
    op.alter_column(
        "users",
        "create_at",
        existing_type=sa.DateTime(timezone=True),
        type_=sa.DateTime(),
        existing_nullable=False,
        existing_server_default=sa.text("now()"),
    )
    op.alter_column("users", "created_at", new_column_name="create_at")

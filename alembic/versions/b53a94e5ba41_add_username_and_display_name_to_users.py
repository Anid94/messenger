"""add username and display_name to users

Revision ID: b53a94e5ba41
Revises: 7efa048cf211
Create Date: 2026-10-03 13:13:50.410082

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'b53a94e5ba41'
down_revision: Union[str, Sequence[str], None] = '7efa048cf211'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column("users", sa.Column("username", sa.String(length=32), nullable=True))
    op.add_column("users", sa.Column("display_name", sa.String(length=64), nullable=True))

    op.execute(
        """
        UPDATE users
        SET username = 'user' || id,
            display_name = split_part(email, '@', 1)
        WHERE username IS NULL
        """
    )

    op.alter_column("users", "username", existing_type=sa.String(length=32), nullable=False)
    op.alter_column("users", "display_name", existing_type=sa.String(length=64), nullable=False)
    op.create_unique_constraint("uq_users_username", "users", ["username"])


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_constraint("uq_users_username", "users", type_="unique")
    op.drop_column("users", "display_name")
    op.drop_column("users", "username")

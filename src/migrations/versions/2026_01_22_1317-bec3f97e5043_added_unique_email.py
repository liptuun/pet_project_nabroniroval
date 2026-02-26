"""added unique email

Revision ID: bec3f97e5043
Revises: c97443a328f0
Create Date: 2026-01-22 13:17:30.290482

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "bec3f97e5043"
down_revision: Union[str, Sequence[str], None] = "c97443a328f0"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.alter_column(
        "users",
        "hashed_password",
        existing_type=sa.VARCHAR(length=200),
        type_=sa.String(length=71),
        existing_nullable=False,
    )


def downgrade() -> None:
    op.alter_column(
        "users",
        "hashed_password",
        existing_type=sa.String(length=71),
        type_=sa.VARCHAR(length=200),
        existing_nullable=False,
    )

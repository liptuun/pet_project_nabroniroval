"""added unique email

Revision ID: bec3f97e5043
Revises: c97443a328f0
Create Date: 2026-01-22 13:17:30.290482

"""

from typing import Sequence, Union

from alembic import op


# revision identifiers, used by Alembic.
revision: str = "bec3f97e5043"
down_revision: Union[str, Sequence[str], None] = "c97443a328f0"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_unique_constraint(None, "users", ["email"])


def downgrade() -> None:
    op.drop_constraint(None, "users", type_="unique")

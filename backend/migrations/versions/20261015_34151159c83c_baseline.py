"""baseline

Empty starting point for the schema. Every later migration builds on this one.

Revision ID: 34151159c83c
Revises:
Create Date: 2026-10-15 18:12:17.684871

"""

from collections.abc import Sequence

# revision identifiers, used by Alembic.
revision: str = "34151159c83c"
down_revision: str | Sequence[str] | None = None
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass

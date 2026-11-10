"""add categories table

Revision ID: dd325fa61698
Revises: 34151159c83c
Create Date: 2026-11-08 14:15:42.742243

"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "dd325fa61698"
down_revision: str | Sequence[str] | None = "34151159c83c"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:

    op.create_table(
        "categories",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(length=100), nullable=False),
        sa.Column("slug", sa.String(length=120), nullable=False),
        sa.Column("image_path", sa.String(length=255), nullable=True),
        sa.Column("position", sa.Integer(), nullable=False),
        sa.Column('is_visible', sa.Boolean(), server_default=sa.false(), nullable=False),
        sa.Column("created_at", sa.DateTime(), server_default=sa.text("now()"), nullable=False),
        sa.Column("updated_at", sa.DateTime(), server_default=sa.text("now()"), nullable=False),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_categories")),
        sa.UniqueConstraint("slug", name="uq_categories_slug"),
    )


def downgrade() -> None:
    op.drop_table("categories")

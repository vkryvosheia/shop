"""add product photos table

Revision ID: f8cac15e6878
Revises: 6a76c81ebd43
Create Date: 2026-11-13 11:03:29.911273

"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "f8cac15e6878"
down_revision: str | Sequence[str] | None = "6a76c81ebd43"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:

    op.create_table(
        "product_photos",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("product_id", sa.Integer(), nullable=False),
        sa.Column("file_path", sa.String(length=255), nullable=False),
        sa.Column("position", sa.Integer(), nullable=False),
        sa.Column(
            "created_at", sa.DateTime(), server_default=sa.text("CURRENT_TIMESTAMP"), nullable=False
        ),
        sa.ForeignKeyConstraint(
            ["product_id"],
            ["products.id"],
            name=op.f("fk_product_photos_product_id_products"),
            ondelete="CASCADE",
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_product_photos")),
    )

    op.create_index(
        op.f("ix_product_photos_product_id"), "product_photos", ["product_id"], unique=False
    )


def downgrade() -> None:
    op.drop_table("product_photos")

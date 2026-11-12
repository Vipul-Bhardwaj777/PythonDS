"""revoked tokens

Revision ID: b7e4a1c92d08
Revises: 96990ef8c131
Create Date: 2026-10-29 15:10:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "b7e4a1c92d08"
down_revision: Union[str, Sequence[str], None] = "96990ef8c131"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "revoked_tokens",
        sa.Column("jti", sa.String(), nullable=False),
        sa.Column("expires_at", sa.DateTime(timezone=True), nullable=False),
        sa.PrimaryKeyConstraint("jti"),
    )


def downgrade() -> None:
    op.drop_table("revoked_tokens")

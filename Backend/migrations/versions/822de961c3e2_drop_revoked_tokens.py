"""drop revoked tokens

Revision ID: 822de961c3e2
Revises: b7e4a1c92d08
Create Date: 2026-11-12 13:18:48.212201

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '822de961c3e2'
down_revision: Union[str, Sequence[str], None] = 'b7e4a1c92d08'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.drop_table("revoked_tokens")


def downgrade() -> None:
    op.create_table(
        "revoked_tokens",
        sa.Column("jti", sa.String(), nullable=False),
        sa.Column("expires_at", sa.DateTime(timezone=True), nullable=False),
        sa.PrimaryKeyConstraint("jti"),
    )

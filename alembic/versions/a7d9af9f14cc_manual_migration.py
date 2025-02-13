"""manual migration

Revision ID: a7d9af9f14cc
Revises: 1e3021d54b23
Create Date: 2025-02-12 14:37:39.722941

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'a7d9af9f14cc'
down_revision: Union[str, None] = '1e3021d54b23'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass

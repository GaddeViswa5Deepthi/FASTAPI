"""add last few columns to posts table

Revision ID: 1e3021d54b23
Revises: 813242fd7dcd
Create Date: 2025-02-12 13:40:34.746629

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.sql.expression import func


# revision identifiers, used by Alembic.
revision: str = '1e3021d54b23'
down_revision: Union[str, None] = '813242fd7dcd'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

def upgrade() :
    op.add_column('posts', sa.Column('published', sa.Boolean(),server_default='TRUE', nullable=False))
    op.add_column('posts',sa.Column('created_at',sa.TIMESTAMP(timezone=True),nullable=False,server_default=func.now()))
    pass



def downgrade() :
    op.drop_column('posts','published')
    op.drop_column('posts','created_at')
    pass

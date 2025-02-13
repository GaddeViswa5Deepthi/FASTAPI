"""add content column to posts

Revision ID: 2aa2555955fe
Revises: dbe9eb3de8a7
Create Date: 2025-02-12 13:21:39.723046

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '2aa2555955fe'
down_revision: Union[str, None] = 'dbe9eb3de8a7'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() :
    op.add_column('posts',sa.Column('content',sa.String(),nullable=False))
    pass


def downgrade():
    op.drop_column('posts','content')
    pass

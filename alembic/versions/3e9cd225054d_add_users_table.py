"""add users table

Revision ID: 3e9cd225054d
Revises: 2aa2555955fe
Create Date: 2025-02-12 13:25:10.844346

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.sql.expression import func

# revision identifiers, used by Alembic.
revision: str = '3e9cd225054d'
down_revision: Union[str, None] = '2aa2555955fe'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.create_table('users',sa.Column('id',sa.Integer(),nullable=False),
    sa.Column('email',sa.String(),nullable=False),
    sa.Column("password",sa.String(),nullable=False),
    sa.Column("created_at",sa.TIMESTAMP(timezone=True),nullable=False,server_default=func.now()),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email'))




def downgrade() :
    op.drop_table('users')
    pass

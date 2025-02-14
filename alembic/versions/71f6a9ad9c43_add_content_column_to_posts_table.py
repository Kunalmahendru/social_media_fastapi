"""add content column to posts table

Revision ID: 71f6a9ad9c43
Revises: e2cdc75a760a
Create Date: 2025-02-10 18:54:41.699161

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '71f6a9ad9c43'
down_revision: Union[str, None] = 'e2cdc75a760a'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.add_column('posts',sa.Column('content',sa.String(),nullable=False))
    pass


def downgrade():
    op.drop_column('posts','content')
    pass

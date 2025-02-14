"""create posts table

Revision ID: e2cdc75a760a
Revises: 
Create Date: 2025-02-10 18:43:04.874413

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'e2cdc75a760a'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.create_table('posts',sa.Column('id',sa.Integer(),nullable=False,primary_key=True)
   ,sa.Column('Title',sa.String(),nullable=False,primary_key=False))
    pass


def downgrade():
    op.drop_table('posts')
    pass

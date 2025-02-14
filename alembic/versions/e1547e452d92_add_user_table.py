"""add user table

Revision ID: e1547e452d92
Revises: 71f6a9ad9c43
Create Date: 2025-02-10 20:31:02.304661

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'e1547e452d92'
down_revision: Union[str, None] = '71f6a9ad9c43'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.create_table('users'
                    ,sa.Column('id',sa.Integer(),nullable=False,primary_key=True)
                    ,sa.Column('email',sa.String(),nullable=False,primary_key=False)
                    ,sa.Column('password',sa.String(),nullable=False,primary_key=False)
                    ,sa.Column('created_at',sa.TIMESTAMP('now()'),nullable=False)
                    ,sa.PrimaryKeyConstraint('id')
                    ,sa.UniqueConstraint('email'))
    pass


def downgrade():
    op.drop_table('users')
    pass

"""add foreign key to post table

Revision ID: cccf8d41b3ab
Revises: e1547e452d92
Create Date: 2025-02-10 20:37:42.013272

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'cccf8d41b3ab'
down_revision: Union[str, None] = 'e1547e452d92'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.add_column('posts',sa.Column('owner_id',sa.Integer(),nullable=False))
    op.create_foreign_key('posts_users_fk',source_table="posts",referent_table="users",local_cols=['owner_id'],remote_cols=['id'],ondelete="cascade")
    pass


def downgrade():
    op.drop_constraint('posts_users_fk',table_name="posts",type_="foreignkey")
    op.drop_column('posts','owner_id')
    pass

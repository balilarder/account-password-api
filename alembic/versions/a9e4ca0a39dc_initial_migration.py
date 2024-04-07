"""Initial migration

Revision ID: a9e4ca0a39dc
Revises: 
Create Date: 2024-04-07 13:33:35.859659

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'a9e4ca0a39dc'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('fail_counter', sa.Integer(), nullable=True))
    op.add_column('users', sa.Column('lock_until', sa.DateTime(), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('users', 'lock_until')
    op.drop_column('users', 'fail_counter')
    # ### end Alembic commands ###
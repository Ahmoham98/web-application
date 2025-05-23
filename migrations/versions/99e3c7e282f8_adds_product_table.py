"""adds product table

Revision ID: 99e3c7e282f8
Revises: 6b228f422078
Create Date: 2025-05-11 08:39:26.512851

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
import sqlmodel


# revision identifiers, used by Alembic.
revision: str = '99e3c7e282f8'
down_revision: Union[str, None] = '6b228f422078'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index('idx_categories_title', table_name='categories')
    op.drop_index('idx_categories_uid', table_name='categories')
    op.create_index(op.f('ix_categories_title'), 'categories', ['title'], unique=False)
    op.create_index(op.f('ix_categories_uid'), 'categories', ['uid'], unique=True)
    # ### end Alembic commands ###


def downgrade() -> None:
    """Downgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_categories_uid'), table_name='categories')
    op.drop_index(op.f('ix_categories_title'), table_name='categories')
    op.create_index('idx_categories_uid', 'categories', ['uid'], unique=False)
    op.create_index('idx_categories_title', 'categories', ['title'], unique=False)
    # ### end Alembic commands ###

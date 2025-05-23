"""remove unneccessary model payments

Revision ID: a6a281d7aa39
Revises: 36bf198f7f22
Create Date: 2025-05-17 15:50:47.293659

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
import sqlmodel
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = 'a6a281d7aa39'
down_revision: Union[str, None] = '36bf198f7f22'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index('ix_payments_uid', table_name='payments')
    op.drop_table('payments')
    # ### end Alembic commands ###


def downgrade() -> None:
    """Downgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('payments',
    sa.Column('uid', sa.UUID(), autoincrement=False, nullable=False),
    sa.Column('order_uid', sa.UUID(), autoincrement=False, nullable=False),
    sa.Column('user_uid', sa.UUID(), autoincrement=False, nullable=False),
    sa.Column('amount', sa.DOUBLE_PRECISION(precision=53), autoincrement=False, nullable=True),
    sa.Column('status', postgresql.ENUM(name="<class 'schema.payment.Status'>"), autoincrement=False, nullable=True),
    sa.Column('payment_method', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('created_at', postgresql.TIMESTAMP(), autoincrement=False, nullable=True),
    sa.ForeignKeyConstraint(['order_uid'], ['orders.uid'], name='payments_order_uid_fkey'),
    sa.ForeignKeyConstraint(['user_uid'], ['users.uid'], name='payments_user_uid_fkey'),
    sa.PrimaryKeyConstraint('uid', name='payments_pkey')
    )
    op.create_index('ix_payments_uid', 'payments', ['uid'], unique=True)
    # ### end Alembic commands ###

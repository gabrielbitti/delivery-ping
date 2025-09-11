"""create table route_customer

Revision ID: b85a1152e04a
Revises: afef1d17c623
Create Date: 2025-09-10 22:01:54.007183

"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = 'b85a1152e04a'
down_revision: Union[str, Sequence[str], None] = 'afef1d17c623'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade."""
    op.create_table('route_customer',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('route_id', sa.Integer(), nullable=False),
        sa.Column('customer_id', sa.Integer(), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=True),
        sa.ForeignKeyConstraint(['customer_id'], ['customer.id'], ),
        sa.ForeignKeyConstraint(['route_id'], ['route.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_route_customer_id'), 'route_customer', ['id'], unique=False)


def downgrade() -> None:
    """Downgrade."""
    op.drop_index(op.f('ix_route_customer_id'), table_name='route_customer')
    op.drop_table('route_customer')

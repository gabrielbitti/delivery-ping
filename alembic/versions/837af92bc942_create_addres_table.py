"""create_addres_table

Revision ID: 837af92bc942
Revises: 34f7d5428a19
Create Date: 2025-09-10 21:50:41.616888

"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = '837af92bc942'
down_revision: Union[str, Sequence[str], None] = '34f7d5428a19'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade."""
    op.create_table('address',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('customer_id', sa.Integer(), nullable=False),
        sa.Column('complete_address', sa.String(), nullable=True),
        sa.Column('city', sa.String(), nullable=False),
        sa.Column('state', sa.String(), nullable=False),
        sa.Column('country', sa.String(), nullable=False),
        sa.Column('zip_code', sa.String(), nullable=True),
        sa.Column('latitude', sa.String(), nullable=True),
        sa.Column('longitude', sa.String(), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=True),
        sa.ForeignKeyConstraint(['customer_id'], ['customer.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_address_id'), 'address', ['id'], unique=False)


def downgrade() -> None:
    """Downgrade."""
    op.drop_index(op.f('ix_address_id'), table_name='address')
    op.drop_table('address')

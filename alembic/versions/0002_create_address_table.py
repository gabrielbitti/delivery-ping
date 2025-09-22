"""create address table

Revision ID: 0002
Revises: 0001
Create Date: 2025-09-22 20:33:19.597618

"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = '0002'
down_revision: Union[str, Sequence[str], None] = '0001'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade."""
    op.create_table('address',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('customer_id', sa.Integer(), nullable=False),
        sa.Column('complete_address', sa.String(length=500), nullable=False),
        sa.Column('city', sa.String(length=100), nullable=False),
        sa.Column('state', sa.String(length=50), nullable=False),
        sa.Column('country', sa.String(length=50), nullable=True),
        sa.Column('zip_code', sa.String(length=10), nullable=True),
        sa.Column('latitude', sa.Float(), nullable=True),
        sa.Column('longitude', sa.Float(), nullable=True),
        sa.Column('is_primary', sa.Boolean(), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=True),
        sa.CheckConstraint('latitude >= -90 AND latitude <= 90', name='valid_latitude'),
        sa.CheckConstraint('longitude >= -180 AND longitude <= 180', name='valid_longitude'),
        sa.ForeignKeyConstraint(['customer_id'], ['customer.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index('idx_address_city_customer', 'address', ['city', 'customer_id'], unique=False)
    op.create_index('idx_address_coordinates', 'address', ['latitude', 'longitude'], unique=False)
    op.create_index('idx_one_primary_address', 'address', ['customer_id'], unique=True, postgresql_where=sa.text('is_primary = true'))
    op.create_index(op.f('ix_address_city'), 'address', ['city'], unique=False)


def downgrade() -> None:
    """Downgrade."""
    op.drop_index(op.f('ix_address_city'), table_name='address')
    op.drop_index('idx_one_primary_address', table_name='address', postgresql_where=sa.text('is_primary = true'))
    op.drop_index('idx_address_coordinates', table_name='address')
    op.drop_index('idx_address_city_customer', table_name='address')
    op.drop_table('address')

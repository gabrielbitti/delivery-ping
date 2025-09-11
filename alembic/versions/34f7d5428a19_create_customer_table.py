"""create_customer_table

Revision ID: 34f7d5428a19
Revises: 
Create Date: 2025-09-10 21:48:30.572939

"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = '34f7d5428a19'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade."""
    op.create_table('customer',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('complete_name', sa.String(), nullable=True),
        sa.Column('nickname', sa.String(), nullable=True),
        sa.Column('cellphone', sa.String(length=20), nullable=True),
        sa.Column('has_whatsapp', sa.Boolean(), nullable=True),
        sa.Column('cpf', sa.String(), nullable=True),
        sa.Column('cnpj', sa.String(), nullable=True),
        sa.Column('email', sa.String(), nullable=True),
        sa.Column('is_active', sa.Boolean(), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_customer_id'), 'customer', ['id'], unique=False)


def downgrade() -> None:
    """Downgrade."""
    op.drop_index(op.f('ix_customer_id'), table_name='customer')
    op.drop_table('customer')

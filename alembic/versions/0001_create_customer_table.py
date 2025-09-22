"""create customer table

Revision ID: 0001
Revises: 
Create Date: 2025-09-22 20:32:49.226834

"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = '0001'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade."""
    op.create_table('customer',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('complete_name', sa.String(length=255), nullable=False),
        sa.Column('nickname', sa.String(length=100), nullable=True),
        sa.Column('cellphone', sa.String(length=20), nullable=False),
        sa.Column('has_whatsapp', sa.Boolean(), nullable=True),
        sa.Column('cpf', sa.String(length=11), nullable=True),
        sa.Column('cnpj', sa.String(length=14), nullable=True),
        sa.Column('email', sa.String(length=255), nullable=True),
        sa.Column('is_active', sa.Boolean(), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=True),
        sa.PrimaryKeyConstraint('id'),
        comment='Tabela de clientes do sistema'
    )
    op.create_index('idx_customer_active_name', 'customer', ['is_active', 'complete_name'], unique=False)
    op.create_index(op.f('ix_customer_cnpj'), 'customer', ['cnpj'], unique=True)
    op.create_index(op.f('ix_customer_cpf'), 'customer', ['cpf'], unique=True)
    op.create_index(op.f('ix_customer_email'), 'customer', ['email'], unique=True)


def downgrade() -> None:
    """Downgrade."""
    op.drop_index(op.f('ix_customer_email'), table_name='customer')
    op.drop_index(op.f('ix_customer_cpf'), table_name='customer')
    op.drop_index(op.f('ix_customer_cnpj'), table_name='customer')
    op.drop_index('idx_customer_active_name', table_name='customer')
    op.drop_table('customer')

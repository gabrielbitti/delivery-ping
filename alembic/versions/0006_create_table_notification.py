"""create table notification

Revision ID: 0006
Revises: 0005
Create Date: 2025-09-10 22:14:39.549257

"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = '0006'
down_revision: Union[str, Sequence[str], None] = '0005'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade."""
    op.create_table('notification',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('customer_id', sa.Integer(), nullable=False),
        sa.Column('route_schedule_id', sa.Integer(), nullable=False),
        sa.Column('type', sa.Enum('PRE_ROUTE', 'CONFIRMATION', name='notification_type'), nullable=False),
        sa.Column('status', sa.Enum('PENDING', 'SENT', 'ERROR', name='notification_status'), nullable=False),
        sa.Column('scheduled_date', sa.String(), nullable=True),
        sa.Column('sent_date', sa.DateTime(timezone=True), nullable=True),
        sa.Column('message', sa.String(), nullable=True),
        sa.Column('customer_response', sa.String(), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=True),
        sa.ForeignKeyConstraint(['customer_id'], ['customer.id'], ),
        sa.ForeignKeyConstraint(['route_schedule_id'], ['route_schedule.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_notification_id'), 'notification', ['id'], unique=False)


def downgrade() -> None:
    """Downgrade."""
    op.drop_index(op.f('ix_notification_id'), table_name='notification')
    op.drop_table('notification')

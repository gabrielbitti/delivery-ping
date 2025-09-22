"""create notification table

Revision ID: 0004
Revises: 0003
Create Date: 2025-09-22 20:35:02.280304

"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = '0004'
down_revision: Union[str, Sequence[str], None] = '0003'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade."""
    op.create_table('notification',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('route_schedule_id', sa.Integer(), nullable=False),
        sa.Column('customer_id', sa.Integer(), nullable=False),
        sa.Column('type', sa.Enum('REMINDER', 'CONFIRMATION', 'CANCELLATION', name='notification_type_enum'), nullable=False),
        sa.Column('status', sa.Enum('PENDING', 'SENT', 'DELIVERED', 'FAILED', name='notification_status_enum'), nullable=False),
        sa.Column('scheduled_date', sa.DateTime(timezone=True), nullable=False),
        sa.Column('sent_date', sa.DateTime(timezone=True), nullable=True),
        sa.Column('message', sa.Text(), nullable=False),
        sa.Column('customer_response', sa.Text(), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=True),
        sa.CheckConstraint('sent_date IS NULL OR sent_date >= scheduled_date', name='valid_sent_date'),
        sa.ForeignKeyConstraint(['customer_id'], ['customer.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['route_schedule_id'], ['route_schedule.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index('idx_notification_pending', 'notification', ['scheduled_date', 'status'], unique=False, postgresql_where="status IN ('PENDING', 'FAILED')")
    op.create_index(op.f('ix_notification_scheduled_date'), 'notification', ['scheduled_date'], unique=False)
    op.create_index(op.f('ix_notification_status'), 'notification', ['status'], unique=False)


def downgrade() -> None:
    """Downgrade."""
    op.drop_index(op.f('ix_notification_status'), table_name='notification')
    op.drop_index(op.f('ix_notification_scheduled_date'), table_name='notification')
    op.drop_index('idx_notification_pending', table_name='notification', postgresql_where="status IN ('pending', 'failed')")
    op.drop_table('notification')
    # if your model creates an ENUM, don't forget to drop it:
    op.execute("DROP TYPE IF EXISTS notification_type_enum;")
    op.execute("DROP TYPE IF EXISTS notification_status_enum;")


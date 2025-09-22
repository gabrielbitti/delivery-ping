"""create route tables

Revision ID: 0003
Revises: 0002
Create Date: 2025-09-22 20:34:25.912201

"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = '0003'
down_revision: Union[str, Sequence[str], None] = '0002'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade."""
    op.create_table('route',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(length=255), nullable=False),
        sa.Column('is_active', sa.Boolean(), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index('idx_route_active', 'route', ['is_active'], unique=False)
    op.create_index(op.f('ix_route_id'), 'route', ['id'], unique=False)
    op.create_table('route_schedule',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('route_id', sa.Integer(), nullable=False),
        sa.Column('status', sa.Enum('PENDING', 'CONFIRMED', 'IN_PROGRESS', 'COMPLETED', 'CANCELLED', name='route_status_enum'), nullable=False),
        sa.Column('schedule_date', sa.DateTime(timezone=True), nullable=False),
        sa.Column('finish_date', sa.DateTime(timezone=True), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=True),
        sa.CheckConstraint('finish_date IS NULL OR finish_date > schedule_date', name='valid_finish_date'),
        sa.ForeignKeyConstraint(['route_id'], ['route.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index('idx_schedule_date_status', 'route_schedule', ['schedule_date', 'status'], unique=False)
    op.create_index(op.f('ix_route_schedule_id'), 'route_schedule', ['id'], unique=False)
    op.create_index(op.f('ix_route_schedule_schedule_date'), 'route_schedule', ['schedule_date'], unique=False)
    op.create_index(op.f('ix_route_schedule_status'), 'route_schedule', ['status'], unique=False)
    op.create_table('route_point',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('route_id', sa.Integer(), nullable=False),
        sa.Column('address_id', sa.Integer(), nullable=False),
        sa.Column('sequence_order', sa.Integer(), nullable=False),
        sa.Column('estimated_time', sa.Integer(), nullable=True),
        sa.Column('distance_to_next', sa.Float(), nullable=True),
        sa.Column('notes', sa.Text(), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=True),
        sa.CheckConstraint('sequence_order > 0', name='positive_sequence'),
        sa.ForeignKeyConstraint(['address_id'], ['address.id'], ondelete='RESTRICT'),
        sa.ForeignKeyConstraint(['route_id'], ['route.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('route_id', 'address_id', name='uq_route_address'),
        sa.UniqueConstraint('route_id', 'sequence_order', name='uq_route_sequence')
    )
    op.create_index('idx_route_point_composite', 'route_point', ['route_id', 'sequence_order'], unique=False)
    op.create_index(op.f('ix_route_point_id'), 'route_point', ['id'], unique=False)


def downgrade() -> None:
    """Downgrade."""
    op.drop_index(op.f('ix_route_point_id'), table_name='route_point')
    op.drop_index('idx_route_point_composite', table_name='route_point')
    op.drop_table('route_point')
    op.drop_index(op.f('ix_route_schedule_status'), table_name='route_schedule')
    op.drop_index(op.f('ix_route_schedule_schedule_date'), table_name='route_schedule')
    op.drop_index(op.f('ix_route_schedule_id'), table_name='route_schedule')
    op.drop_index('idx_schedule_date_status', table_name='route_schedule')
    op.drop_table('route_schedule')
    op.drop_index(op.f('ix_route_id'), table_name='route')
    op.drop_index('idx_route_active', table_name='route')
    op.drop_table('route')
    # if your model creates an ENUM, don't forget to drop it:
    op.execute("DROP TYPE IF EXISTS route_status_enum;")


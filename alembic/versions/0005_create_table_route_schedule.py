"""create table route_schedule

Revision ID: 0005
Revises: 0004
Create Date: 2025-09-10 22:09:56.689144

"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = '0005'
down_revision: Union[str, Sequence[str], None] = '0004'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade."""
    op.create_table('route_schedule',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('route_id', sa.Integer(), nullable=False),
        sa.Column('status', sa.Enum('PLANNED', 'IN_PROGRESS', 'COMPLETED', name='route_schedule_status'), nullable=False),
        sa.Column('schedule_date', sa.DateTime(timezone=True), nullable=True),
        sa.Column('finish_date', sa.DateTime(timezone=True), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=True),
        sa.ForeignKeyConstraint(['route_id'], ['route.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_route_schedule_id'), 'route_schedule', ['id'], unique=False)


def downgrade() -> None:
    """Downgrade."""
    op.drop_index(op.f('ix_route_schedule_id'), table_name='route_schedule')
    op.drop_table('route_schedule')

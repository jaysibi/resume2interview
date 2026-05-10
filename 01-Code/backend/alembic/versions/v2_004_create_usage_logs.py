"""create usage_logs table for rate limiting analytics

Revision ID: v2_004
Revises: v2_003
Create Date: 2026-05-07

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = 'v2_004'
down_revision = 'v2_003'
branch_labels = None
depends_on = None


def upgrade():
    """Create usage_logs table for tracking API usage and rate limiting"""
    op.create_table(
        'usage_logs',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('ip_address', sa.String(length=50), nullable=False),
        sa.Column('user_agent', sa.Text(), nullable=True),
        sa.Column('endpoint', sa.String(length=255), nullable=False),
        sa.Column('method', sa.String(length=10), nullable=False),
        sa.Column('status_code', sa.Integer(), nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=True),
        sa.Column('rate_limited', sa.Integer(), server_default='0', nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='SET NULL'),
        sa.PrimaryKeyConstraint('id')
    )
    
    # Create indexes for performance
    op.create_index('ix_usage_logs_id', 'usage_logs', ['id'])
    op.create_index('ix_usage_logs_ip_address', 'usage_logs', ['ip_address'])
    op.create_index('ix_usage_logs_user_id', 'usage_logs', ['user_id'])
    op.create_index('ix_usage_logs_created_at', 'usage_logs', ['created_at'])
    op.create_index('idx_ip_date', 'usage_logs', ['ip_address', 'created_at'])
    op.create_index('idx_date_endpoint', 'usage_logs', ['created_at', 'endpoint'])


def downgrade():
    """Drop usage_logs table"""
    op.drop_index('idx_date_endpoint', table_name='usage_logs')
    op.drop_index('idx_ip_date', table_name='usage_logs')
    op.drop_index('ix_usage_logs_created_at', table_name='usage_logs')
    op.drop_index('ix_usage_logs_user_id', table_name='usage_logs')
    op.drop_index('ix_usage_logs_ip_address', table_name='usage_logs')
    op.drop_index('ix_usage_logs_id', table_name='usage_logs')
    op.drop_table('usage_logs')

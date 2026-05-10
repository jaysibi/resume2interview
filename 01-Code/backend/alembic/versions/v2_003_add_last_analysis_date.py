"""add last_analysis_date to users

Revision ID: v2_003
Revises: v2_002
Create Date: 2026-05-04

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = 'v2_003'
down_revision = 'v2_002'
branch_labels = None
depends_on = None


def upgrade():
    """Add last_analysis_date column to users table"""
    op.add_column('users', sa.Column('last_analysis_date', sa.DateTime(timezone=True), nullable=True))


def downgrade():
    """Remove last_analysis_date column from users table"""
    op.drop_column('users', 'last_analysis_date')

"""add user contact and job info fields

Revision ID: v2_002
Revises: v2_001
Create Date: 2026-05-04

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = 'v2_002'
down_revision = 'v2_001'
branch_labels = None
depends_on = None


def upgrade():
    """Add contact and professional information fields to users table"""
    # Add new columns to users table
    op.add_column('users', sa.Column('last_title', sa.String(length=255), nullable=True))
    op.add_column('users', sa.Column('last_company', sa.String(length=255), nullable=True))
    op.add_column('users', sa.Column('job_applying_for', sa.String(length=255), nullable=True))
    op.add_column('users', sa.Column('ats_summary_score', sa.Integer(), nullable=True))
    op.add_column('users', sa.Column('missing_skills', sa.JSON(), nullable=True, server_default='[]'))


def downgrade():
    """Remove contact and professional information fields from users table"""
    op.drop_column('users', 'missing_skills')
    op.drop_column('users', 'ats_summary_score')
    op.drop_column('users', 'job_applying_for')
    op.drop_column('users', 'last_company')
    op.drop_column('users', 'last_title')

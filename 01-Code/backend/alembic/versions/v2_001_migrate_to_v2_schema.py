"""migrate_to_v2_schema

Revision ID: v2_001
Revises: 
Create Date: 2026-05-03

Migration from V1 to V2 schema:
- Creates users table
- Creates applications table  
- Creates gap_analyses table
- Creates ats_scores table
- Modifies resumes table (add user_id, upload_date, remove created_at)
- Modifies job_descriptions table (add user_id, job_url, title, company, upload_date, remove created_at)
- Migrates existing data to default user
"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql
from sqlalchemy import text

# revision identifiers, used by Alembic.
revision = 'v2_001'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    """Upgrade to V2 schema"""
    
    # 1. Create users table
    op.create_table(
        'users',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(length=255), nullable=False),
        sa.Column('email', sa.String(length=255), nullable=False),
        sa.Column('phone', sa.String(length=50), nullable=True),
        sa.Column('password_hash', sa.String(length=255), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_users_id'), 'users', ['id'], unique=False)
    op.create_index(op.f('ix_users_email'), 'users', ['email'], unique=True)
    
    # Insert default user for existing data
    op.execute("""
        INSERT INTO users (name, email, created_at, updated_at)
        VALUES ('Default User', 'default@resumetailor.local', now(), now())
    """)
    
    # 2. Add new columns to resumes table (check if they exist first)
    # Note: tools column already exists in V1, so we skip it
    conn = op.get_bind()
    inspector = sa.inspect(conn)
    existing_columns = [c['name'] for c in inspector.get_columns('resumes')]
    
    if 'user_id' not in existing_columns:
        op.add_column('resumes', sa.Column('user_id', sa.Integer(), nullable=True))
    if 'upload_date' not in existing_columns:
        op.add_column('resumes', sa.Column('upload_date', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True))
    # tools column already exists in V1, skip it
    
    # Set user_id for existing resumes to default user (id=1)
    op.execute("UPDATE resumes SET user_id = 1 WHERE user_id IS NULL")
    op.execute("UPDATE resumes SET upload_date = created_at WHERE upload_date IS NULL AND created_at IS NOT NULL")
    
    # Make user_id NOT NULL and add foreign key
    op.alter_column('resumes', 'user_id', nullable=False)
    op.create_foreign_key('fk_resumes_user_id', 'resumes', 'users', ['user_id'], ['id'], ondelete='CASCADE')
    op.create_index(op.f('ix_resumes_user_id'), 'resumes', ['user_id'], unique=False)
    
    # 3. Add new columns to job_descriptions table (check if they exist first)
    existing_jd_columns = [c['name'] for c in inspector.get_columns('job_descriptions')]
    
    if 'user_id' not in existing_jd_columns:
        op.add_column('job_descriptions', sa.Column('user_id', sa.Integer(), nullable=True))
    if 'job_url' not in existing_jd_columns:
        op.add_column('job_descriptions', sa.Column('job_url', sa.String(length=1000), nullable=True))
    if 'title' not in existing_jd_columns:
        op.add_column('job_descriptions', sa.Column('title', sa.String(length=500), nullable=True))
    if 'company' not in existing_jd_columns:
        op.add_column('job_descriptions', sa.Column('company', sa.String(length=500), nullable=True))
    if 'upload_date' not in existing_jd_columns:
        op.add_column('job_descriptions', sa.Column('upload_date', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True))
    
    # Set user_id for existing job_descriptions to default user (id=1)
    op.execute("UPDATE job_descriptions SET user_id = 1 WHERE user_id IS NULL")
    op.execute("UPDATE job_descriptions SET upload_date = created_at WHERE upload_date IS NULL AND created_at IS NOT NULL")
    
    # Make user_id NOT NULL and add foreign key
    op.alter_column('job_descriptions', 'user_id', nullable=False)
    op.create_foreign_key('fk_job_descriptions_user_id', 'job_descriptions', 'users', ['user_id'], ['id'], ondelete='CASCADE')
    op.create_index(op.f('ix_job_descriptions_user_id'), 'job_descriptions', ['user_id'], unique=False)
    
    # 4. Create applications table
    op.create_table(
        'applications',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('resume_id', sa.Integer(), nullable=False),
        sa.Column('jd_id', sa.Integer(), nullable=False),
        sa.Column('applied_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
        sa.Column('status', sa.String(length=50), server_default='analyzed', nullable=True),
        sa.Column('notes', sa.Text(), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['resume_id'], ['resumes.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['jd_id'], ['job_descriptions.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_applications_id'), 'applications', ['id'], unique=False)
    op.create_index(op.f('ix_applications_user_id'), 'applications', ['user_id'], unique=False)
    op.create_index(op.f('ix_applications_resume_id'), 'applications', ['resume_id'], unique=False)
    op.create_index(op.f('ix_applications_jd_id'), 'applications', ['jd_id'], unique=False)
    op.create_index('idx_user_applied_at', 'applications', ['user_id', 'applied_at'], unique=False)
    
    # 5. Create gap_analyses table
    op.create_table(
        'gap_analyses',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('application_id', sa.Integer(), nullable=False),
        sa.Column('match_score', sa.Integer(), nullable=False),
        sa.Column('missing_required_skills', postgresql.JSON(astext_type=sa.Text()), server_default='[]', nullable=True),
        sa.Column('missing_preferred_skills', postgresql.JSON(astext_type=sa.Text()), server_default='[]', nullable=True),
        sa.Column('strengths', postgresql.JSON(astext_type=sa.Text()), server_default='[]', nullable=True),
        sa.Column('weak_areas', postgresql.JSON(astext_type=sa.Text()), server_default='[]', nullable=True),
        sa.Column('recommendations', postgresql.JSON(astext_type=sa.Text()), server_default='[]', nullable=True),
        sa.Column('detailed_analysis', sa.Text(), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
        sa.ForeignKeyConstraint(['application_id'], ['applications.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('application_id')
    )
    op.create_index(op.f('ix_gap_analyses_id'), 'gap_analyses', ['id'], unique=False)
    op.create_index(op.f('ix_gap_analyses_application_id'), 'gap_analyses', ['application_id'], unique=True)
    
    # 6. Create ats_scores table
    op.create_table(
        'ats_scores',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('application_id', sa.Integer(), nullable=False),
        sa.Column('ats_score', sa.Integer(), nullable=False),
        sa.Column('keyword_match_percentage', sa.Integer(), nullable=False),
        sa.Column('format_score', sa.Integer(), nullable=False),
        sa.Column('matched_keywords', postgresql.JSON(astext_type=sa.Text()), server_default='[]', nullable=True),
        sa.Column('missing_keywords', postgresql.JSON(astext_type=sa.Text()), server_default='[]', nullable=True),
        sa.Column('issues', postgresql.JSON(astext_type=sa.Text()), server_default='[]', nullable=True),
        sa.Column('recommendations', postgresql.JSON(astext_type=sa.Text()), server_default='[]', nullable=True),
        sa.Column('detailed_analysis', sa.Text(), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
        sa.ForeignKeyConstraint(['application_id'], ['applications.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('application_id')
    )
    op.create_index(op.f('ix_ats_scores_id'), 'ats_scores', ['id'], unique=False)
    op.create_index(op.f('ix_ats_scores_application_id'), 'ats_scores', ['application_id'], unique=True)


def downgrade():
    """Downgrade from V2 to V1 schema (CAUTION: Data loss will occur)"""
    
    # Drop new tables
    op.drop_index(op.f('ix_ats_scores_application_id'), table_name='ats_scores')
    op.drop_index(op.f('ix_ats_scores_id'), table_name='ats_scores')
    op.drop_table('ats_scores')
    
    op.drop_index(op.f('ix_gap_analyses_application_id'), table_name='gap_analyses')
    op.drop_index(op.f('ix_gap_analyses_id'), table_name='gap_analyses')
    op.drop_table('gap_analyses')
    
    op.drop_index('idx_user_applied_at', table_name='applications')
    op.drop_index(op.f('ix_applications_jd_id'), table_name='applications')
    op.drop_index(op.f('ix_applications_resume_id'), table_name='applications')
    op.drop_index(op.f('ix_applications_user_id'), table_name='applications')
    op.drop_index(op.f('ix_applications_id'), table_name='applications')
    op.drop_table('applications')
    
    # Remove new columns from job_descriptions
    op.drop_index(op.f('ix_job_descriptions_user_id'), table_name='job_descriptions')
    op.drop_constraint('fk_job_descriptions_user_id', 'job_descriptions', type_='foreignkey')
    op.drop_column('job_descriptions', 'upload_date')
    op.drop_column('job_descriptions', 'company')
    op.drop_column('job_descriptions', 'title')
    op.drop_column('job_descriptions', 'job_url')
    op.drop_column('job_descriptions', 'user_id')
    
    # Remove new columns from resumes (but keep tools as it was in V1)
    op.drop_index(op.f('ix_resumes_user_id'), table_name='resumes')
    op.drop_constraint('fk_resumes_user_id', 'resumes', type_='foreignkey')
    # tools column exists in V1, don't drop it
    op.drop_column('resumes', 'upload_date')
    op.drop_column('resumes', 'user_id')
    
    # Drop users table
    op.drop_index(op.f('ix_users_email'), table_name='users')
    op.drop_index(op.f('ix_users_id'), table_name='users')
    op.drop_table('users')

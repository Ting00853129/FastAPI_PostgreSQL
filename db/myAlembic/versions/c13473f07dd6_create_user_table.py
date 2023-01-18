"""create user table

Revision ID: c13473f07dd6
Revises: 
Create Date: 2023-01-17 00:20:40.605951

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c13473f07dd6'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'user',
        sa.Column('username', sa.String, primary_key = True),
        sa.Column('password', sa.String, nullable = False),
        sa.Column('birthday', sa.Date),
        sa.Column('create_time', sa.DateTime, default=sa.func.datetime.utcnow),
        sa.Column('last_login', sa.DateTime, nullable = True)
    )


def downgrade():
    op.drop_table('user')

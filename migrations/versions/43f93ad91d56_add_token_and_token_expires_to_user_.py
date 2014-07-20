"""add token and token_expires to user table

Revision ID: 43f93ad91d56
Revises: None
Create Date: 2014-07-20 12:37:56.672371

"""

# revision identifiers, used by Alembic.
revision = '43f93ad91d56'
down_revision = None

from alembic import op
import sqlalchemy as sa

def upgrade():
    op.add_column('user', sa.Column('token', sa.String(120)))
    op.add_column('user', sa.Column('token_expires', sa.DateTime))

def downgrade():
    op.drop_column('user', 'token')
    op.drop_column('user', 'token_expires')

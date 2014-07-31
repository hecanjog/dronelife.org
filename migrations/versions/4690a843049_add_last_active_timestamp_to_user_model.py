"""add last active timestamp to user model

Revision ID: 4690a843049
Revises: 27aad5730793
Create Date: 2014-07-31 02:17:00.346262

"""

# revision identifiers, used by Alembic.
revision = '4690a843049'
down_revision = '27aad5730793'

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.add_column('user', sa.Column('last_active', sa.DateTime))


def downgrade():
    op.drop_column('user', 'last_active')

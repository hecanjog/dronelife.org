"""add last post to thread model

Revision ID: 508a39871281
Revises: 43f93ad91d56
Create Date: 2014-07-22 11:28:21.243786

"""

# revision identifiers, used by Alembic.
revision = '508a39871281'
down_revision = '43f93ad91d56'

from alembic import op
import sqlalchemy as sa

def upgrade():
    op.add_column('thread', sa.Column('last_post_id', sa.Integer, sa.ForeignKey('post.id')))
    op.add_column('thread', sa.Column('updated', sa.DateTime))

def downgrade():
    op.drop_column('thread', 'last_post_id')
    op.drop_column('thread', 'updated')

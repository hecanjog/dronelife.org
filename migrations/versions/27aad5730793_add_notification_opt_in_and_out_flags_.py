"""add notification opt in and out flags to user model

Revision ID: 27aad5730793
Revises: 508a39871281
Create Date: 2014-07-30 17:32:06.679616

"""

# revision identifiers, used by Alembic.
revision = '27aad5730793'
down_revision = '508a39871281'

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.add_column('user', sa.Column('enable_mailing_list', sa.Boolean))
    op.add_column('user', sa.Column('enable_at_reply_notifications', sa.Boolean))
    op.add_column('user', sa.Column('enable_direct_reply_notifications', sa.Boolean))
    op.add_column('user', sa.Column('enable_created_threads_notifications', sa.Boolean))
    op.add_column('user', sa.Column('enable_participated_threads_notifications', sa.Boolean))

def downgrade():
    op.drop_column('user', 'enable_mailing_list')
    op.drop_column('user', 'enable_at_reply_notifications')
    op.drop_column('user', 'enable_direct_reply_notifications')
    op.drop_column('user', 'enable_created_threads_notifications')
    op.drop_column('user', 'enable_participated_threads_notifications')

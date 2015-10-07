"""email migration

Revision ID: 1e40103807fb
Revises: 4fd506e671ae
Create Date: 2015-10-06 17:18:03.352621

"""

# revision identifiers, used by Alembic.
revision = '1e40103807fb'
down_revision = '4fd506e671ae'

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('email', sa.String(length=64), nullable=True))
    op.create_index('ix_users_email', 'users', ['email'], unique=True)
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_index('ix_users_email', 'users')
    op.drop_column('users', 'email')
    ### end Alembic commands ###

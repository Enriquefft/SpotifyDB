"""initial migration

Revision ID: 7607fdb6286a
Revises: 
Create Date: 2022-10-14 13:40:06.745606

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '7607fdb6286a'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    from sqlalchemy import column, table
    op.add_column('users', sa.Column('auth_level', sa.SmallInteger(), nullable=True))
    role = table('users', column('auth_level'))
    op.execute(role.update().values(auth_level=0))
    op.alter_column('users', 'auth_level', nullable=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('users', 'auth_level')
    # ### end Alembic commands ###

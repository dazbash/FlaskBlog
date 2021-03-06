"""empty message

Revision ID: ae692818a820
Revises: b49057dd81e5
Create Date: 2019-12-31 20:35:31.767718

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = 'ae692818a820'
down_revision = 'b49057dd81e5'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('uzers',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('email', sa.String(length=128), nullable=False),
    sa.Column('password', sa.String(length=128), nullable=False),
    sa.Column('role', sa.Integer(), nullable=False),
    sa.Column('full_name', sa.String(length=128), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email')
    )
    op.drop_index('email', table_name='users')
    op.drop_table('users')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('users',
    sa.Column('id', mysql.INTEGER(display_width=11), autoincrement=True, nullable=False),
    sa.Column('email', mysql.VARCHAR(length=128), nullable=False),
    sa.Column('password', mysql.VARCHAR(length=32), nullable=False),
    sa.Column('role', mysql.INTEGER(display_width=11), autoincrement=False, nullable=False),
    sa.Column('full_name', mysql.VARCHAR(length=128), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    mysql_default_charset=u'utf8mb4',
    mysql_engine=u'InnoDB'
    )
    op.create_index('email', 'users', ['email'], unique=True)
    op.drop_table('uzers')
    # ### end Alembic commands ###

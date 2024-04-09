"""empty message

Revision ID: d3e243b3c911
Revises: 
Create Date: 2024-04-09 12:52:13.996228

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd3e243b3c911'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('login',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('access_code', sa.Integer(), nullable=True),
    sa.Column('email_address', sa.String(length=500), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('users',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('first_name', sa.String(length=1000), nullable=True),
    sa.Column('last_name', sa.String(length=1000), nullable=True),
    sa.Column('email_address', sa.String(length=500), nullable=True),
    sa.Column('mobile', sa.String(length=30), nullable=True),
    sa.Column('home_address', sa.String(length=1000), nullable=True),
    sa.Column('url_of_picture', sa.String(length=1000), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('users')
    op.drop_table('login')
    # ### end Alembic commands ###

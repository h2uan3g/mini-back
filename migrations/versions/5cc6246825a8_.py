"""empty message

Revision ID: 5cc6246825a8
Revises: 44bf9a499dda
Create Date: 2024-12-04 20:31:50.949937

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '5cc6246825a8'
down_revision = '44bf9a499dda'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('healths',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('type', sa.Integer(), nullable=True),
    sa.Column('title', sa.String(length=64), nullable=True),
    sa.Column('auth', sa.String(length=64), nullable=True),
    sa.Column('body', sa.Text(), nullable=True),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_healths')),
    sa.UniqueConstraint('type', name=op.f('uq_healths_type'))
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('healths')
    # ### end Alembic commands ###

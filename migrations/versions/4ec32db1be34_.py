"""empty message

Revision ID: 4ec32db1be34
Revises: 5cc6246825a8
Create Date: 2024-12-06 15:24:45.717628

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '4ec32db1be34'
down_revision = '5cc6246825a8'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('healths', schema=None) as batch_op:
        batch_op.add_column(sa.Column('coverImage', sa.String(length=64), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('healths', schema=None) as batch_op:
        batch_op.drop_column('coverImage')

    # ### end Alembic commands ###

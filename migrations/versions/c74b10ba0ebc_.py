"""empty message

Revision ID: c74b10ba0ebc
Revises: 045b0d792b6a
Create Date: 2025-01-22 09:55:35.816645

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c74b10ba0ebc'
down_revision = '045b0d792b6a'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('documents', schema=None) as batch_op:
        batch_op.drop_column('create_time')
        batch_op.drop_column('update_time')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('documents', schema=None) as batch_op:
        batch_op.add_column(sa.Column('update_time', sa.DATETIME(), nullable=True))
        batch_op.add_column(sa.Column('create_time', sa.DATETIME(), nullable=True))

    # ### end Alembic commands ###

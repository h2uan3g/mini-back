"""empty message

Revision ID: c56ef55a62e2
Revises: 2d09c6e803bb
Create Date: 2025-01-16 20:30:39.807184

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c56ef55a62e2'
down_revision = '2d09c6e803bb'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('news', schema=None) as batch_op:
        batch_op.add_column(sa.Column('fk_news_newstype', sa.Integer(), nullable=True))
        batch_op.create_foreign_key(batch_op.f('fk_news_fk_news_newstype_news_types'), 'news_types', ['fk_news_newstype'], ['id'])

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('news', schema=None) as batch_op:
        batch_op.drop_constraint(batch_op.f('fk_news_fk_news_newstype_news_types'), type_='foreignkey')
        batch_op.drop_column('fk_news_newstype')

    # ### end Alembic commands ###

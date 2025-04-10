"""Add front_img and back_img to Card

Revision ID: 7840a4716c6c
Revises: 4dab8c2e1741
Create Date: 2025-03-26 20:00:01.564471

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '7840a4716c6c'
down_revision = '4dab8c2e1741'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('card', schema=None) as batch_op:
        batch_op.add_column(sa.Column('front_img', sa.Text(), nullable=True))
        batch_op.add_column(sa.Column('back_img', sa.Text(), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('card', schema=None) as batch_op:
        batch_op.drop_column('back_img')
        batch_op.drop_column('front_img')

    # ### end Alembic commands ###

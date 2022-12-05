"""empty message

Revision ID: 03be390f6304
Revises: 037facacb993
Create Date: 2022-12-05 17:31:46.100288

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '03be390f6304'
down_revision = '037facacb993'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user', sa.Column('session_count', sa.Integer(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('user', 'session_count')
    # ### end Alembic commands ###
"""empty message

Revision ID: 26b39b8868a4
Revises: 41bffcdf1764
Create Date: 2015-12-15 15:56:36.145442

"""

# revision identifiers, used by Alembic.
revision = '26b39b8868a4'
down_revision = '41bffcdf1764'

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.add_column('publications', sa.Column('additional_source_string', sa.Text(), nullable=True))
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('publications', 'additional_source_string')
    ### end Alembic commands ###

"""empty message

Revision ID: 4188b309c94f
Revises: 17215eafe5cb
Create Date: 2015-12-09 11:58:03.313007

"""

# revision identifiers, used by Alembic.
revision = '4188b309c94f'
down_revision = '17215eafe5cb'

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    pass
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.create_index('species_ibfk_2', 'species', ['iucn_status_id'], unique=False)
    op.create_index('species_ibfk_1', 'species', ['esa_status_id'], unique=False)
    op.add_column('matrices', sa.Column('periodicity_id', mysql.INTEGER(display_width=11), nullable=True))
    op.drop_column('matrices', 'periodicity')
    op.create_table('periodicities',
    sa.Column('id', mysql.INTEGER(display_width=11), nullable=False),
    sa.Column('name', mysql.VARCHAR(length=64), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    mysql_default_charset=u'utf8',
    mysql_engine=u'InnoDB'
    )
    ### end Alembic commands ###
"""empty message

Revision ID: f631efd4af14
Revises: cece6bb94374
Create Date: 2022-02-15 15:14:54.315782

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f631efd4af14'
down_revision = 'cece6bb94374'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint('favoriteplanet_ibfk_1', 'favoriteplanet', type_='foreignkey')
    op.drop_constraint('favoriteplanet_ibfk_2', 'favoriteplanet', type_='foreignkey')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_foreign_key('favoriteplanet_ibfk_2', 'favoriteplanet', 'user', ['user_id'], ['id'])
    op.create_foreign_key('favoriteplanet_ibfk_1', 'favoriteplanet', 'planet', ['planet_id'], ['planet_id'])
    # ### end Alembic commands ###

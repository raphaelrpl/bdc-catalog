"""edit enums

Revision ID: 566a05da999d
Revises: be5ae740887a
Create Date: 2020-11-27 11:58:58.900865

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '566a05da999d'
down_revision = 'be5ae740887a'
branch_labels = ()
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.get_bind().connect() as conn:
        conn.execute('COMMIT')
        for value in ('classification', 'mosaic'):
            conn.execute("ALTER TYPE public.collection_type ADD VALUE '%s'" % (
                value
            ))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    ''' TODO: '''
    # ### end Alembic commands ###
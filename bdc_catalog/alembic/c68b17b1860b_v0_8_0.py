"""v0.8.0.

Revision ID: c68b17b1860b
Revises: 566a05da999d
Create Date: 2020-12-10 19:47:22.326893
"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c68b17b1860b'
down_revision = '566a05da999d'
branch_labels = ()
depends_on = 'e8b12ba52665'  # LCCS-DB reference id


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('collections', sa.Column('classification_system_id', sa.Integer(), nullable=True), schema='bdc')
    op.create_foreign_key(op.f('collections_classification_system_id_class_systems_fkey'), 'collections', 'class_systems', ['classification_system_id'], ['id'], source_schema='bdc', referent_schema='lccs', onupdate='CASCADE', ondelete='CASCADE')
    op.create_index(op.f('idx_bdc_collections_classification_system_id'), 'collections', ['classification_system_id'],
                    unique=False, schema='bdc')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('idx_bdc_collections_classification_system_id'), table_name='collections', schema='bdc')
    op.drop_constraint(op.f('collections_classification_system_id_class_systems_fkey'), 'collections', schema='bdc', type_='foreignkey')
    op.drop_column('collections', 'classification_system_id', schema='bdc')
    # ### end Alembic commands ###

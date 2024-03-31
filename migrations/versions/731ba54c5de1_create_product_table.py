"""Create product table

Revision ID: 731ba54c5de1
Revises: 
Create Date: 2024-01-28 18:10:05.909379

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '731ba54c5de1'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('product', schema=None) as batch_op:
        batch_op.add_column(sa.Column('generic_name', sa.String(length=255), nullable=True))
        batch_op.add_column(sa.Column('brands', sa.String(length=255), nullable=True))
        batch_op.add_column(sa.Column('categories', sa.String(length=255), nullable=True))
        batch_op.add_column(sa.Column('ingredients_text', sa.Text(), nullable=True))
        batch_op.add_column(sa.Column('labels', sa.String(length=255), nullable=True))
        batch_op.add_column(sa.Column('product_name', sa.String(length=255), nullable=True))
        batch_op.add_column(sa.Column('quantity', sa.String(length=255), nullable=True))
        batch_op.add_column(sa.Column('image_url', sa.String(length=255), nullable=True))
        batch_op.add_column(sa.Column('proteins', sa.Float(), nullable=True))
        batch_op.add_column(sa.Column('fiber', sa.Float(), nullable=True))
        batch_op.add_column(sa.Column('energy', sa.Float(), nullable=True))
        batch_op.add_column(sa.Column('sugars', sa.Float(), nullable=True))
        batch_op.add_column(sa.Column('saturated_fat', sa.Float(), nullable=True))
        batch_op.add_column(sa.Column('sodium', sa.Float(), nullable=True))
        batch_op.alter_column('id',
               existing_type=mysql.INTEGER(),
               type_=sa.String(length=255),
               existing_nullable=False)
        batch_op.drop_index('name')
        batch_op.drop_column('consommation_qte')
        batch_op.drop_column('production_qte')
        batch_op.drop_column('category')
        batch_op.drop_column('type')
        batch_op.drop_column('wilaya')
        batch_op.drop_column('name')

    with op.batch_alter_table('produit', schema=None) as batch_op:
        batch_op.alter_column('id',
               existing_type=mysql.INTEGER(),
               type_=sa.String(length=255),
               existing_nullable=False)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('produit', schema=None) as batch_op:
        batch_op.alter_column('id',
               existing_type=sa.String(length=255),
               type_=mysql.INTEGER(),
               existing_nullable=False)

    with op.batch_alter_table('product', schema=None) as batch_op:
        batch_op.add_column(sa.Column('name', mysql.VARCHAR(length=150), nullable=True))
        batch_op.add_column(sa.Column('wilaya', mysql.VARCHAR(length=150), nullable=True))
        batch_op.add_column(sa.Column('type', mysql.VARCHAR(length=150), nullable=True))
        batch_op.add_column(sa.Column('category', mysql.VARCHAR(length=150), nullable=True))
        batch_op.add_column(sa.Column('production_qte', mysql.INTEGER(), autoincrement=False, nullable=True))
        batch_op.add_column(sa.Column('consommation_qte', mysql.INTEGER(), autoincrement=False, nullable=True))
        batch_op.create_index('name', ['name'], unique=True)
        batch_op.alter_column('id',
               existing_type=sa.String(length=255),
               type_=mysql.INTEGER(),
               existing_nullable=False)
        batch_op.drop_column('sodium')
        batch_op.drop_column('saturated_fat')
        batch_op.drop_column('sugars')
        batch_op.drop_column('energy')
        batch_op.drop_column('fiber')
        batch_op.drop_column('proteins')
        batch_op.drop_column('image_url')
        batch_op.drop_column('quantity')
        batch_op.drop_column('product_name')
        batch_op.drop_column('labels')
        batch_op.drop_column('ingredients_text')
        batch_op.drop_column('categories')
        batch_op.drop_column('brands')
        batch_op.drop_column('generic_name')

    # ### end Alembic commands ###

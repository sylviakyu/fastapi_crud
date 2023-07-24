"""create init db

Revision ID: 0caf697f26e2
Revises: 
Create Date: 2023-07-24 13:37:56.066655

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql


# revision identifiers, used by Alembic.
revision = '0caf697f26e2'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    ## setting table
    add_data_table_dict = {}

    # [ADD] 'lot_file_setting' table
    size = op.create_table('size',
    sa.Column('id', mysql.INTEGER(1), autoincrement=True, nullable=False),
    sa.Column('name', sa.String(length=5), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    add_data_table_dict["size"] = size

    color = op.create_table('color',
    sa.Column('id', mysql.INTEGER(3), autoincrement=True, nullable=False),
    sa.Column('name', sa.String(length=10), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    add_data_table_dict["color"] = color

    category = op.create_table('category',
    sa.Column('id', mysql.INTEGER(3), autoincrement=True, nullable=False),
    sa.Column('name', sa.String(length=10), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    add_data_table_dict["category"] = category

    op.create_table('item',
    sa.Column('id', mysql.INTEGER(5), autoincrement=True, nullable=False),
    sa.Column('category_id', mysql.INTEGER(3), nullable=False),
    sa.Column('name', sa.String(length=10), nullable=False),
    sa.Column('code', sa.String(length=10), nullable=False),
    sa.Column('price', sa.Float, nullable=False),
    sa.ForeignKeyConstraint(['category_id'], ['category.id'], name='fk_item_category_id'),
    sa.PrimaryKeyConstraint('id')
    )

    op.create_table('item_size',
    sa.Column('item_id', mysql.INTEGER(5), nullable=False),
    sa.Column('size_id', mysql.INTEGER(1), nullable=False),
    sa.ForeignKeyConstraint(['item_id'], ['item.id'], name='fk_item_size_item_id'),
    sa.ForeignKeyConstraint(['size_id'], ['size.id'], name='fk_item_size_size_id'),
    sa.PrimaryKeyConstraint('item_id', 'size_id')
    )

    op.create_table('item_color',
    sa.Column('item_id', mysql.INTEGER(5), nullable=False),
    sa.Column('color_id', mysql.INTEGER(3), nullable=False),
    sa.ForeignKeyConstraint(['item_id'], ['item.id'], name='fk_item_color_item_id'),
    sa.ForeignKeyConstraint(['color_id'], ['color.id'], name='fk_item_color_color_id'),
    sa.PrimaryKeyConstraint('item_id', 'color_id')
    )


def downgrade() -> None:
    pass

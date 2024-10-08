"""Добавил атрибут скидки в таблицу товаров

Revision ID: 7621a98ad776
Revises: 5231dcf2c593
Create Date: 2024-06-19 17:13:56.558311

"""

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "7621a98ad776"
down_revision = "5231dcf2c593"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column("Product", sa.Column("product_discount", sa.Integer(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column("Product", "product_discount")
    # ### end Alembic commands ###

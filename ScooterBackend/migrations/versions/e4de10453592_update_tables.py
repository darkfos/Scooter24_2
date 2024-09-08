"""Update tables

Revision ID: e4de10453592
Revises: 162f1975f418
Create Date: 2024-09-05 21:23:10.738127

"""

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "e4de10453592"
down_revision = "162f1975f418"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(
        "Product_id_category_fkey", "Product", type_="foreignkey"
    )
    op.drop_column("Product", "id_category")
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column(
        "Product",
        sa.Column(
            "id_category", sa.INTEGER(), autoincrement=False, nullable=False
        ),
    )
    op.create_foreign_key(
        "Product_id_category_fkey",
        "Product",
        "Category",
        ["id_category"],
        ["id"],
    )
    # ### end Alembic commands ###
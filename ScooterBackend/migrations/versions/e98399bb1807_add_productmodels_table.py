"""add productmodels table

Revision ID: e98399bb1807
Revises: 9e6b2ba356cd
Create Date: 2024-10-05 11:54:08.679221

"""

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "e98399bb1807"
down_revision = "9e6b2ba356cd"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "Productmodels",
        sa.Column("id_product", sa.Integer(), nullable=False),
        sa.Column("id_model", sa.Integer(), nullable=False),
        sa.Column("id", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(
            ["id_model"],
            ["Model.id"],
        ),
        sa.ForeignKeyConstraint(
            ["id_product"],
            ["Product.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.drop_constraint("Product_model_fkey", "Product", type_="foreignkey")
    op.drop_column("Product", "model")
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column(
        "Product",
        sa.Column("model", sa.INTEGER(), autoincrement=False, nullable=True),
    )
    op.create_foreign_key(
        "Product_model_fkey", "Product", "Model", ["model"], ["id"]
    )
    op.drop_table("Productmodels")
    # ### end Alembic commands ###
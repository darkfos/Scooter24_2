"""add subcategory tables

Revision ID: 9e6b2ba356cd
Revises: f4e143594c13
Create Date: 2024-10-04 10:21:12.955828

"""

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "9e6b2ba356cd"
down_revision = "f4e143594c13"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "Subsubcategory",
        sa.Column("name", sa.String(length=225), nullable=False),
        sa.Column("id_sub_category", sa.Integer(), nullable=False),
        sa.Column("id", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(
            ["id_sub_category"],
            ["Subcategory.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("name"),
    )
    op.add_column(
        "Product", sa.Column("id_s_sub_category", sa.Integer(), nullable=False)
    )
    op.drop_constraint(
        "Product_id_category_fkey", "Product", type_="foreignkey"
    )
    op.drop_constraint(
        "Product_id_subcategory_thirst_level_fkey",
        "Product",
        type_="foreignkey",
    )
    op.drop_constraint(
        "Product_id_subcategory_second_level_fkey",
        "Product",
        type_="foreignkey",
    )
    op.create_foreign_key(
        None, "Product", "Subsubcategory", ["id_s_sub_category"], ["id"]
    )
    op.drop_column("Product", "id_subcategory_thirst_level")
    op.drop_column("Product", "id_subcategory_second_level")
    op.drop_column("Product", "id_category")
    op.alter_column(
        "Subcategory",
        "id_category",
        existing_type=sa.INTEGER(),
        nullable=False,
    )
    op.create_unique_constraint(None, "Subcategory", ["name"])
    op.drop_constraint(
        "Subcategory_id_sub_category_fkey", "Subcategory", type_="foreignkey"
    )
    op.drop_column("Subcategory", "level")
    op.drop_column("Subcategory", "id_sub_category")
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column(
        "Subcategory",
        sa.Column(
            "id_sub_category", sa.INTEGER(), autoincrement=False, nullable=True
        ),
    )
    op.add_column(
        "Subcategory",
        sa.Column("level", sa.INTEGER(), autoincrement=False, nullable=False),
    )
    op.create_foreign_key(
        "Subcategory_id_sub_category_fkey",
        "Subcategory",
        "Subcategory",
        ["id_sub_category"],
        ["id"],
    )
    op.drop_constraint(None, "Subcategory", type_="unique")
    op.alter_column(
        "Subcategory", "id_category", existing_type=sa.INTEGER(), nullable=True
    )
    op.add_column(
        "Product",
        sa.Column(
            "id_category", sa.INTEGER(), autoincrement=False, nullable=True
        ),
    )
    op.add_column(
        "Product",
        sa.Column(
            "id_subcategory_second_level",
            sa.INTEGER(),
            autoincrement=False,
            nullable=True,
        ),
    )
    op.add_column(
        "Product",
        sa.Column(
            "id_subcategory_thirst_level",
            sa.INTEGER(),
            autoincrement=False,
            nullable=True,
        ),
    )
    op.drop_constraint(None, "Product", type_="foreignkey")
    op.create_foreign_key(
        "Product_id_subcategory_second_level_fkey",
        "Product",
        "Subcategory",
        ["id_subcategory_second_level"],
        ["id"],
    )
    op.create_foreign_key(
        "Product_id_subcategory_thirst_level_fkey",
        "Product",
        "Subcategory",
        ["id_subcategory_thirst_level"],
        ["id"],
    )
    op.create_foreign_key(
        "Product_id_category_fkey",
        "Product",
        "Category",
        ["id_category"],
        ["id"],
    )
    op.drop_column("Product", "id_s_sub_category")
    op.drop_table("Subsubcategory")
    # ### end Alembic commands ###

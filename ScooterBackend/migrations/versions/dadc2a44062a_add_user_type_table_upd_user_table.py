"""add: user_type table; upd: user table

Revision ID: dadc2a44062a
Revises: e98399bb1807
Create Date: 2024-10-11 19:10:02.073524

"""

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "dadc2a44062a"
down_revision = "e98399bb1807"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "Admin",
        sa.Column("email_admin", sa.String(length=150), nullable=False),
        sa.Column("password_user", sa.Text(), nullable=False),
        sa.Column("date_create", sa.Date(), nullable=True),
        sa.Column("date_update", sa.Date(), nullable=True),
        sa.Column("id", sa.Integer(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        op.f("ix_Admin_email_admin"), "Admin", ["email_admin"], unique=True
    )
    op.create_table(
        "Brand",
        sa.Column("name_brand", sa.String(length=100), nullable=False),
        sa.Column("id", sa.Integer(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("name_brand"),
    )
    op.create_table(
        "Category",
        sa.Column("name_category", sa.String(length=150), nullable=False),
        sa.Column("icon_category", sa.Text(), nullable=True),
        sa.Column("id", sa.Integer(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        op.f("ix_Category_name_category"),
        "Category",
        ["name_category"],
        unique=True,
    )
    op.create_table(
        "Mark",
        sa.Column("name_mark", sa.String(length=100), nullable=False),
        sa.Column("id", sa.Integer(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("name_mark"),
    )
    op.create_table(
        "Model",
        sa.Column("name_model", sa.String(length=100), nullable=False),
        sa.Column("id", sa.Integer(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("name_model"),
    )
    op.create_table(
        "Typeworker",
        sa.Column("name_type", sa.String(length=300), nullable=False),
        sa.Column("id", sa.Integer(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        op.f("ix_Typeworker_name_type"),
        "Typeworker",
        ["name_type"],
        unique=True,
    )
    op.create_table(
        "Usertype",
        sa.Column("name_type", sa.String(length=100), nullable=False),
        sa.Column("id", sa.Integer(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "Subcategory",
        sa.Column("name", sa.String(length=225), nullable=False),
        sa.Column("id_category", sa.Integer(), nullable=False),
        sa.Column("id", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(
            ["id_category"],
            ["Category.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("name"),
    )
    op.create_table(
        "User",
        sa.Column("id_type_user", sa.Integer(), nullable=False),
        sa.Column("email_user", sa.Text(), nullable=False),
        sa.Column("password_user", sa.String(length=60), nullable=False),
        sa.Column("secret_update_key", sa.String(length=80), nullable=True),
        sa.Column("name_user", sa.String(length=100), nullable=True),
        sa.Column("surname_user", sa.String(length=150), nullable=True),
        sa.Column("main_name_user", sa.String(length=250), nullable=False),
        sa.Column("date_registration", sa.Date(), nullable=False),
        sa.Column("date_update", sa.Date(), nullable=False),
        sa.Column("name_user_address", sa.String(length=200), nullable=True),
        sa.Column("surname_user_address", sa.String(length=200), nullable=True),
        sa.Column("name_company_address", sa.String(length=200), nullable=True),
        sa.Column("country_address", sa.String(length=300), nullable=True),
        sa.Column("address_street", sa.String(length=450), nullable=True),
        sa.Column("address_rl_et_home", sa.String(length=250), nullable=True),
        sa.Column("address_locality", sa.String(length=300), nullable=True),
        sa.Column("address_area", sa.String(length=350), nullable=True),
        sa.Column("address_index", sa.Integer(), nullable=True),
        sa.Column("address_phone_number", sa.String(length=40), nullable=True),
        sa.Column("id", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(
            ["id_type_user"],
            ["Usertype.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        op.f("ix_User_country_address"),
        "User",
        ["country_address"],
        unique=False,
    )
    op.create_index(
        op.f("ix_User_email_user"), "User", ["email_user"], unique=True
    )
    op.create_index(
        op.f("ix_User_name_company_address"),
        "User",
        ["name_company_address"],
        unique=False,
    )
    op.create_table(
        "Vacancies",
        sa.Column("salary_employee", sa.Integer(), nullable=False),
        sa.Column("description_vacancies", sa.Text(), nullable=False),
        sa.Column("id_type_worker", sa.Integer(), nullable=False),
        sa.Column("id", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(
            ["id_type_worker"],
            ["Typeworker.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
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
    op.create_table(
        "Product",
        sa.Column("article_product", sa.String(length=300), nullable=False),
        sa.Column("title_product", sa.String(length=500), nullable=False),
        sa.Column("brand", sa.Integer(), nullable=True),
        sa.Column("brand_mark", sa.Integer(), nullable=True),
        sa.Column("weight_product", sa.Double(), nullable=True),
        sa.Column("id_s_sub_category", sa.Integer(), nullable=False),
        sa.Column("explanation_product", sa.Text(), nullable=True),
        sa.Column("photo_product", sa.Text(), nullable=True),
        sa.Column("quantity_product", sa.Integer(), nullable=True),
        sa.Column("price_product", sa.Double(), nullable=False),
        sa.Column("price_with_discount", sa.Double(), nullable=True),
        sa.Column("date_create_product", sa.Date(), nullable=True),
        sa.Column("date_update_information", sa.Date(), nullable=True),
        sa.Column("product_discount", sa.Integer(), nullable=True),
        sa.Column("id", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(
            ["brand"],
            ["Brand.id"],
        ),
        sa.ForeignKeyConstraint(
            ["brand_mark"],
            ["Mark.id"],
        ),
        sa.ForeignKeyConstraint(
            ["id_s_sub_category"],
            ["Subsubcategory.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        op.f("ix_Product_title_product"),
        "Product",
        ["title_product"],
        unique=True,
    )
    op.create_table(
        "Favourite",
        sa.Column("id_user", sa.Integer(), nullable=False),
        sa.Column("id_product", sa.Integer(), nullable=False),
        sa.Column("id", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(
            ["id_product"],
            ["Product.id"],
        ),
        sa.ForeignKeyConstraint(
            ["id_user"],
            ["User.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "Historybuy",
        sa.Column("id_user", sa.Integer(), nullable=False),
        sa.Column("id_product", sa.Integer(), nullable=False),
        sa.Column("id", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(
            ["id_product"],
            ["Product.id"],
        ),
        sa.ForeignKeyConstraint(
            ["id_user"],
            ["User.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "Order",
        sa.Column("date_buy", sa.Date(), nullable=False),
        sa.Column("id_user", sa.Integer(), nullable=False),
        sa.Column("id_product", sa.Integer(), nullable=False),
        sa.Column("id", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(
            ["id_product"],
            ["Product.id"],
        ),
        sa.ForeignKeyConstraint(
            ["id_user"],
            ["User.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
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
    op.create_table(
        "Review",
        sa.Column("text_review", sa.Text(), nullable=False),
        sa.Column("estimation_review", sa.Integer(), nullable=False),
        sa.Column("id_user", sa.Integer(), nullable=False),
        sa.Column("id_product", sa.Integer(), nullable=False),
        sa.Column("id", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(
            ["id_product"],
            ["Product.id"],
        ),
        sa.ForeignKeyConstraint(
            ["id_user"],
            ["User.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table("Review")
    op.drop_table("Productmodels")
    op.drop_table("Order")
    op.drop_table("Historybuy")
    op.drop_table("Favourite")
    op.drop_index(op.f("ix_Product_title_product"), table_name="Product")
    op.drop_table("Product")
    op.drop_table("Subsubcategory")
    op.drop_table("Vacancies")
    op.drop_index(op.f("ix_User_name_company_address"), table_name="User")
    op.drop_index(op.f("ix_User_email_user"), table_name="User")
    op.drop_index(op.f("ix_User_country_address"), table_name="User")
    op.drop_table("User")
    op.drop_table("Subcategory")
    op.drop_table("Usertype")
    op.drop_index(op.f("ix_Typeworker_name_type"), table_name="Typeworker")
    op.drop_table("Typeworker")
    op.drop_table("Model")
    op.drop_table("Mark")
    op.drop_index(op.f("ix_Category_name_category"), table_name="Category")
    op.drop_table("Category")
    op.drop_table("Brand")
    op.drop_index(op.f("ix_Admin_email_admin"), table_name="Admin")
    op.drop_table("Admin")
    # ### end Alembic commands ###

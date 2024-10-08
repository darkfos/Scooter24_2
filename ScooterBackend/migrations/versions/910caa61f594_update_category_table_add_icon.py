"""update category table, add icon

Revision ID: 910caa61f594
Revises: aef13943eb3a
Create Date: 2024-09-24 23:50:06.766504

"""

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "910caa61f594"
down_revision = "aef13943eb3a"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column(
        "Category", sa.Column("icon_category", sa.Text(), nullable=True)
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column("Category", "icon_category")
    # ### end Alembic commands ###

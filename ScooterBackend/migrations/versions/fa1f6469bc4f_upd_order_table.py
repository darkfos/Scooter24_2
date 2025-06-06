"""upd: order table

Revision ID: fa1f6469bc4f
Revises: b8bf6dfa3bc3
Create Date: 2025-05-02 18:40:42.238839

"""

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "fa1f6469bc4f"
down_revision = "b8bf6dfa3bc3"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column("Order", sa.Column("label_order", sa.UUID(), nullable=True))
    op.add_column("Order", sa.Column("address", sa.Text(), nullable=True))
    op.create_unique_constraint(None, "Order", ["label_order"])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, "Order", type_="unique")
    op.drop_column("Order", "address")
    op.drop_column("Order", "label_order")
    # ### end Alembic commands ###

"""Added Admin tabel

Revision ID: 3f762e395067
Revises: 6db9e4973704
Create Date: 2024-06-04 15:33:34.556326

"""

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "3f762e395067"
down_revision = "6db9e4973704"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "Admin",
        sa.Column("email_admin", sa.String(length=150), nullable=True),
        sa.Column("password_user", sa.Text(), nullable=True),
        sa.Column("date_create", sa.Date(), nullable=False),
        sa.Column("date_update", sa.Date(), nullable=False),
        sa.Column("id", sa.Integer(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("email_admin"),
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table("Admin")
    # ### end Alembic commands ###

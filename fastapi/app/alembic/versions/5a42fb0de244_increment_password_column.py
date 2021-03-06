"""increment password column

Revision ID: 5a42fb0de244
Revises: 678e35c47327
Create Date: 2022-07-28 12:58:22.165834

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = "5a42fb0de244"
down_revision = "678e35c47327"
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column(
        "products",
        "origin_img",
        existing_type=mysql.LONGBLOB(),
        type_=sa.LargeBinary(length=16777216),
        existing_nullable=False,
    )
    op.alter_column(
        "products",
        "rounded_square_icon",
        existing_type=mysql.LONGBLOB(),
        type_=sa.LargeBinary(length=16777216),
        existing_nullable=True,
    )
    op.alter_column(
        "products",
        "circle_icon",
        existing_type=mysql.LONGBLOB(),
        type_=sa.LargeBinary(length=16777216),
        existing_nullable=True,
    )
    op.alter_column(
        "users",
        "password",
        existing_type=mysql.VARCHAR(length=50),
        type_=sa.String(length=60),
        existing_nullable=False,
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column(
        "users",
        "password",
        existing_type=sa.String(length=60),
        type_=mysql.VARCHAR(length=50),
        existing_nullable=False,
    )
    op.alter_column(
        "products",
        "circle_icon",
        existing_type=sa.LargeBinary(length=16777216),
        type_=mysql.LONGBLOB(),
        existing_nullable=True,
    )
    op.alter_column(
        "products",
        "rounded_square_icon",
        existing_type=sa.LargeBinary(length=16777216),
        type_=mysql.LONGBLOB(),
        existing_nullable=True,
    )
    op.alter_column(
        "products",
        "origin_img",
        existing_type=sa.LargeBinary(length=16777216),
        type_=mysql.LONGBLOB(),
        existing_nullable=False,
    )
    # ### end Alembic commands ###

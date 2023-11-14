"""rename relevance column name

Revision ID: caa65671a03b
Revises: eeb907413006
Create Date: 2023-11-13 19:26:47.158645

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "caa65671a03b"
down_revision = "eeb907413006"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table("analytics", schema=None) as batch_op:
        batch_op.add_column(sa.Column("relevance", sa.Integer(), nullable=True))
        batch_op.add_column(sa.Column("added", sa.DateTime(), nullable=True))
        batch_op.add_column(sa.Column("published", sa.DateTime(), nullable=True))
        batch_op.drop_column("published_at")
        batch_op.drop_column("relavance")
        batch_op.drop_column("added_at")

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table("analytics", schema=None) as batch_op:
        batch_op.add_column(sa.Column("added_at", sa.DATETIME(), nullable=True))
        batch_op.add_column(sa.Column("relavance", sa.INTEGER(), nullable=True))
        batch_op.add_column(sa.Column("published_at", sa.DATETIME(), nullable=True))
        batch_op.drop_column("published")
        batch_op.drop_column("added")
        batch_op.drop_column("relevance")

    # ### end Alembic commands ###
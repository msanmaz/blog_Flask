"""pst

Revision ID: b868b16cc769
Revises: 6c405dc20759
Create Date: 2020-04-13 04:35:53.734958

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b868b16cc769'
down_revision = '6c405dc20759'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('users', 'password_has',
               existing_type=sa.VARCHAR(length=50),
               nullable=True)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('users', 'password_has',
               existing_type=sa.VARCHAR(length=50),
               nullable=False)
    # ### end Alembic commands ###
"""add update field to purchase model

Revision ID: dd928743cc6f
Revises: 02878f6430e4
Create Date: 2024-05-21 10:27:10.998502

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'dd928743cc6f'
down_revision: Union[str, None] = '02878f6430e4'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('purchase', sa.Column('update_date', sa.DateTime(), server_default=sa.text('now()'), nullable=False))
    op.drop_column('purchase_list', 'id')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('purchase_list', sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False))
    op.drop_column('purchase', 'update_date')
    # ### end Alembic commands ###

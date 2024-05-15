"""add category_id

Revision ID: 56bced70819d
Revises: 057b66d06ed4
Create Date: 2024-05-15 11:44:23.650469

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '56bced70819d'
down_revision: Union[str, None] = '057b66d06ed4'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('product', sa.Column('category_id', sa.Integer(), nullable=False))
    op.create_foreign_key(None, 'product', 'category', ['category_id'], ['id'], ondelete='CASCADE')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'product', type_='foreignkey')
    op.drop_column('product', 'category_id')
    # ### end Alembic commands ###

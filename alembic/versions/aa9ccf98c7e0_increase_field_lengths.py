"""increase field lengths

Revision ID: aa9ccf98c7e0
Revises: 31f014d6102e
Create Date: 2025-04-06 19:38:34.595226

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'aa9ccf98c7e0'
down_revision: Union[str, None] = '31f014d6102e'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('user', 'description',
               existing_type=sa.VARCHAR(length=50),
               type_=sa.String(length=3000),
               existing_nullable=True)
    op.alter_column('user', 'img',
               existing_type=sa.VARCHAR(length=50),
               type_=sa.String(length=3000),
               existing_nullable=True)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('user', 'img',
               existing_type=sa.String(length=3000),
               type_=sa.VARCHAR(length=50),
               existing_nullable=True)
    op.alter_column('user', 'description',
               existing_type=sa.String(length=3000),
               type_=sa.VARCHAR(length=50),
               existing_nullable=True)
    # ### end Alembic commands ###

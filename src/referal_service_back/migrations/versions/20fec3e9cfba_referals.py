"""referals

Revision ID: 20fec3e9cfba
Revises: 079ae74dcb81
Create Date: 2024-03-13 22:56:49.847036

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '20fec3e9cfba'
down_revision: Union[str, None] = '079ae74dcb81'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('referal_codes',
    sa.Column('id', sa.UUID(), nullable=False),
    sa.Column('code', sa.String(), nullable=False),
    sa.Column('parent_id', sa.UUID(), nullable=False),
    sa.Column('exp_date', sa.DateTime(), nullable=True),
    sa.Column('is_active', sa.Boolean(), nullable=False),
    sa.ForeignKeyConstraint(['parent_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('referalship',
    sa.Column('id', sa.UUID(), nullable=False),
    sa.Column('code_id', sa.UUID(), nullable=False),
    sa.Column('user_id', sa.UUID(), nullable=False),
    sa.ForeignKeyConstraint(['code_id'], ['referal_codes.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('referalship')
    op.drop_table('referal_codes')
    # ### end Alembic commands ###

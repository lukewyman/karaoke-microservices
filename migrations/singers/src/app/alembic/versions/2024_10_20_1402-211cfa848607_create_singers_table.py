"""create singers table

Revision ID: 211cfa848607
Revises: 87c14dafecd6
Create Date: 2024-10-20 14:02:03.479762

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '211cfa848607'
down_revision: Union[str, None] = '87c14dafecd6'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table('singers',
                    sa.Column('id', sa.Text, primary_key=True),
                    sa.Column('email', sa.Text),
                    sa.Column('first_name', sa.Text),
                    sa.Column('last_name', sa.Text),
                    sa.Column('stage_name', sa.Text),
                    schema='singers'
                    )


def downgrade() -> None:
    op.drop_table('singers', schema='singers')

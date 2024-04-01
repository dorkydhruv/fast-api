"""Add content column

Revision ID: 5348d24c1dc8
Revises: c1a15996417d
Create Date: 2024-04-01 06:37:37.125682

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '5348d24c1dc8'
down_revision: Union[str, None] = 'c1a15996417d'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('posts',sa.Column('content',sa.String(),nullable=False))
    pass


def downgrade() -> None:
    op.drop_column('posts','content')
    pass

"""add phone and status columns

Revision ID: c056aa6c60c6
Revises: 44b2a36d26a5
Create Date: 2025-12-31 20:52:29.564835

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'c056aa6c60c6'
down_revision: Union[str, None] = '44b2a36d26a5'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

from alembic import op
import sqlalchemy as sa

def upgrade():
    op.add_column("clients", sa.Column("phone", sa.String(), nullable=True))
    op.add_column("orders", sa.Column("status", sa.String(), nullable=True))

def downgrade():
    op.drop_column("orders", "status")
    op.drop_column("clients", "phone")

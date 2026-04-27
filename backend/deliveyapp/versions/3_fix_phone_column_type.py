"""fix phone column type to varchar

Revision ID: 3_fix_phone_column_type
Revises: 62a788456d1a
Create Date: 2026-04-09 14:58:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '3_fix_phone_column_type'
down_revision: Union[str, Sequence[str], None] = '62a788456d1a'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.alter_column('shipment', 'client_contact_phone',
               existing_type=sa.Integer(),
               type_=sa.String(),
               existing_nullable=True)


def downgrade() -> None:
    """Downgrade schema."""
    op.alter_column('shipment', 'client_contact_phone',
               existing_type=sa.String(),
               type_=sa.Integer(),
               existing_nullable=True)

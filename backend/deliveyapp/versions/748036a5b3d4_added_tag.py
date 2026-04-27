"""added tag

Revision ID: 748036a5b3d4
Revises: 684105679d64
Create Date: 2026-04-24 14:43:40.470927

"""
from typing import Sequence, Union

import sqlmodel
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql


# revision identifiers, used by Alembic.
revision: str = '748036a5b3d4'
down_revision: Union[str, Sequence[str], None] = '684105679d64'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # --- Create tag table ---
    op.create_table(
        'tag',
        sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('name', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
        sa.Column('description', sqlmodel.sql.sqltypes.AutoString(), nullable=True),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('name'),
    )

    # --- Create shipment_tag join table ---
    op.create_table(
        'shipment_tag',
        sa.Column('shipment_id', sa.Uuid(), nullable=False),
        sa.Column('tag_id', sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(['shipment_id'], ['shipment.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['tag_id'], ['tag.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('shipment_id', 'tag_id'),
    )

    # --- Seed tag table with initial delivery-relevant tags ---
    op.execute(
        """
        INSERT INTO tag (name, description) VALUES
        ('fragile',    'Contents are breakable and require careful handling to prevent damage during transit'),
        ('perishable', 'Contains food or biological material with a limited shelf life that must be delivered promptly'),
        ('express',    'High-priority shipment that must be delivered within the shortest possible timeframe'),
        ('heavy',      'Package exceeds standard weight thresholds and requires additional handling equipment'),
        ('oversized',  'Dimensions exceed standard parcel limits and cannot be processed through normal conveyor systems'),
        ('hazardous',  'Contains dangerous goods such as flammable, corrosive, or toxic materials subject to special regulations'),
        ('cold_chain', 'Temperature-sensitive cargo that must remain within a specified refrigerated range throughout delivery'),
        ('document',   'Contains official papers, contracts, or legal documents that must arrive intact and confidential')
        """
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table('shipment_tag')
    op.drop_table('tag')

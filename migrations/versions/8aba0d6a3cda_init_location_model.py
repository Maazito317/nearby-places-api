"""init_location_model

Revision ID: 8aba0d6a3cda
Revises: 
Create Date: 2025-07-03 18:45:40.258618

"""
from typing import Sequence, Union

from alembic import op
from geoalchemy2 import Geometry
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '8aba0d6a3cda'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table(
        'locations',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('name', sa.String(100)),
        sa.Column('point', Geometry(geometry_type='POINT', srid=4326))
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table('locations')
    # ### end Alembic commands ###

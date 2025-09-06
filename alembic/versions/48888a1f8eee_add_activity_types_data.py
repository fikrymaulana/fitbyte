"""Add activity types data

Revision ID: 48888a1f8eee
Revises: 
Create Date: 2025-09-05 22:14:01.436203

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '48888a1f8eee'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # Insert activity types data
    op.execute("""
    INSERT INTO activity_types (type, calories_per_minute) VALUES
    ('Walking', 4),
    ('Yoga', 4),
    ('Stretching', 4),
    ('Cycling', 8),
    ('Swimming', 8),
    ('Dancing', 8),
    ('Hiking', 10),
    ('Running', 10),
    ('HIIT', 10),
    ('JumpRope', 10)
    """)


def downgrade() -> None:
    """Downgrade schema."""
    # Delete the inserted activity types
    op.execute("""
    DELETE FROM activity_types WHERE type IN (
        'Walking', 'Yoga', 'Stretching', 'Cycling', 'Swimming',
        'Dancing', 'Hiking', 'Running', 'HIIT', 'JumpRope'
    )
    """)

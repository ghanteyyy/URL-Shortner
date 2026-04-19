"""Removed Original Url Table

Revision ID: 274743a36cff
Revises: 0a0bb44b1a14
Create Date: 2026-04-19

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers
revision: str = '274743a36cff'
down_revision: Union[str, Sequence[str], None] = '0a0bb44b1a14'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""

    op.add_column('short_urls', sa.Column('original_url', sa.Text(), nullable=True))
    op.execute("""
        UPDATE short_urls
        SET original_url = original_urls.url
        FROM original_urls
        WHERE short_urls.original_url_id = original_urls.id
    """)

    op.alter_column('short_urls', 'original_url', nullable=False)
    op.drop_constraint(op.f('short_urls_original_url_id_fkey'), 'short_urls', type_='foreignkey')
    op.drop_index(op.f('ix_short_urls_original_url_id'), table_name='short_urls')
    op.drop_column('short_urls', 'original_url_id')
    op.create_index(op.f('ix_short_urls_original_url'), 'short_urls', ['original_url'], unique=False)
    op.drop_index(op.f('ix_original_urls_user_id'), table_name='original_urls')
    op.drop_table('original_urls')


def downgrade() -> None:
    """Downgrade schema."""

    op.create_table('original_urls',
        sa.Column('id', sa.UUID(), nullable=False),
        sa.Column('url', sa.TEXT(), nullable=False),
        sa.Column('created_at', postgresql.TIMESTAMP(), nullable=False),
        sa.Column('user_id', sa.UUID(), nullable=True),
        sa.ForeignKeyConstraint(
            ['user_id'],
            ['users.id'],
            name=op.f('original_urls_user_id_fkey'),
            ondelete='CASCADE'
        ),
        sa.PrimaryKeyConstraint('id', name=op.f('original_urls_pkey'))
    )

    op.create_index(
        op.f('ix_original_urls_user_id'),
        'original_urls',
        ['user_id'],
        unique=False
    )

    op.add_column('short_urls', sa.Column('original_url_id', sa.UUID(), nullable=True))
    op.create_foreign_key(
        op.f('short_urls_original_url_id_fkey'),
        'short_urls',
        'original_urls',
        ['original_url_id'],
        ['id'],
        ondelete='CASCADE'
    )

    op.drop_index(op.f('ix_short_urls_original_url'), table_name='short_urls')
    op.drop_column('short_urls', 'original_url')

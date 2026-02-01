"""manual_init_orders

Revision ID: a6efb7b4a82c
Revises: 
Create Date: 2026-01-18 12:04:17.275820

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = 'a6efb7b4a82c'
down_revision = None
branch_labels = None
depends_on = None

def upgrade() -> None:
    # --- ВСТАВЛЯЕМ ЭТОТ БЛОК ---
    op.create_table(
        'orders',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=True),
        sa.Column('status', sa.String(length=50), nullable=False),
        sa.Column('total_amount', sa.Numeric(precision=10, scale=2), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_orders_id'), 'orders', ['id'], unique=False)
    # ---------------------------

def downgrade() -> None:
    # На случай, если захотим откатить:
    op.drop_index(op.f('ix_orders_id'), table_name='orders')
    op.drop_table('orders')

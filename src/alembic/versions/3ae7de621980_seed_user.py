"""Seed user

Revision ID: 3ae7de621980
Revises: 9bc82f680af1
Create Date: 2023-07-22 21:00:48.012506

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.sql import table
from sqlalchemy.dialects import mysql
import hashlib


# revision identifiers, used by Alembic.
revision = '3ae7de621980'
down_revision = '9bc82f680af1'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.bulk_insert(table=table(
        'users',
        sa.Column('name'),
        sa.Column('username'),
        sa.Column('password'),
        sa.Column('role'),
        sa.Column('flag'),
    ), rows=[
        {
            'name': 'Admin',
            'username': 'admin',
            'password': hashlib.md5(b'admin').hexdigest(),
            'role': 'ADMIN',
            'flag': 1
        },
    ])
    pass


def downgrade() -> None:
    pass

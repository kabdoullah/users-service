"""Création des tables

Revision ID: 8331805a694a
Revises: 0ab1b570105b
Create Date: 2024-08-02 10:51:28.919113

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '8331805a694a'
down_revision: Union[str, None] = '0ab1b570105b'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('sub_categories')
    op.drop_table('categories')
    op.drop_index('ix_profiles_id', table_name='profiles')
    op.drop_table('profiles')
    op.drop_table('profile_rights')
    op.drop_index('ix_rights_id', table_name='rights')
    op.drop_table('rights')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('rights',
    sa.Column('id', sa.NUMERIC(), nullable=False),
    sa.Column('name', sa.VARCHAR(), nullable=False),
    sa.Column('created_at', sa.DATETIME(), nullable=True),
    sa.Column('updated_at', sa.DATETIME(), nullable=True),
    sa.Column('deleted_at', sa.DATETIME(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index('ix_rights_id', 'rights', ['id'], unique=False)
    op.create_table('profile_rights',
    sa.Column('profile_id', sa.NUMERIC(), nullable=False),
    sa.Column('right_id', sa.NUMERIC(), nullable=False),
    sa.ForeignKeyConstraint(['profile_id'], ['profiles.id'], ),
    sa.ForeignKeyConstraint(['right_id'], ['rights.id'], ),
    sa.PrimaryKeyConstraint('profile_id', 'right_id')
    )
    op.create_table('profiles',
    sa.Column('id', sa.NUMERIC(), nullable=False),
    sa.Column('name', sa.VARCHAR(), nullable=False),
    sa.Column('created_at', sa.DATETIME(), nullable=True),
    sa.Column('updated_at', sa.DATETIME(), nullable=True),
    sa.Column('deleted_at', sa.DATETIME(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index('ix_profiles_id', 'profiles', ['id'], unique=False)
    op.create_table('categories',
    sa.Column('id', sa.NUMERIC(), nullable=False),
    sa.Column('name', sa.VARCHAR(), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name')
    )
    op.create_table('sub_categories',
    sa.Column('id', sa.NUMERIC(), nullable=False),
    sa.Column('name', sa.VARCHAR(), nullable=False),
    sa.Column('category_id', sa.NUMERIC(), nullable=True),
    sa.ForeignKeyConstraint(['category_id'], ['categories.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###

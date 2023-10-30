"""Membuat Table Mahasiswa

Revision ID: eafc2cd031b9
Revises: 4afb70717429
Create Date: 2023-10-28 20:57:47.444173

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'eafc2cd031b9'
down_revision = '4afb70717429'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('mahasiswa',
    sa.Column('id', sa.BigInteger(), autoincrement=True, nullable=False),
    sa.Column('nim', sa.String(length=50), nullable=False),
    sa.Column('nama', sa.String(length=50), nullable=False),
    sa.Column('phone', sa.String(length=50), nullable=False),
    sa.Column('prodi', sa.String(length=50), nullable=False),
    sa.Column('alamat', sa.String(length=50), nullable=False),
    sa.Column('dosen_satu', sa.BigInteger(), nullable=True),
    sa.Column('dosen_dua', sa.BigInteger(), nullable=True),
    sa.ForeignKeyConstraint(['dosen_dua'], ['dosen.id'], ),
    sa.ForeignKeyConstraint(['dosen_satu'], ['dosen.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('mahasiswa')
    # ### end Alembic commands ###

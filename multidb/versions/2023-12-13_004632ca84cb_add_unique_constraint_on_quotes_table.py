"""add unique constraint on quotes table

Revision ID: 004632ca84cb
Revises: bfe2eda9cce0
Create Date: 2023-12-13 14:12:23.583481

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '004632ca84cb'
down_revision: Union[str, None] = 'bfe2eda9cce0'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade(engine_name: str) -> None:
    globals()["upgrade_%s" % engine_name]()


def downgrade(engine_name: str) -> None:
    globals()["downgrade_%s" % engine_name]()





def upgrade_postgres_engine() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_unique_constraint(op.f('quotes_quote_uniq_key'), 'quotes', ['quote'])
    # ### end Alembic commands ###


def downgrade_postgres_engine() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(op.f('quotes_quote_uniq_key'), 'quotes', type_='unique')
    # ### end Alembic commands ###


def upgrade_sqlite_engine() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('quotes') as batch_op:
        batch_op.create_unique_constraint(batch_op.f('quotes_quote_uniq_key'), ['quote'])
    # ### end Alembic commands ###


def downgrade_sqlite_engine() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('quotes') as batch_op:
        batch_op.drop_constraint(batch_op.f('quotes_quote_uniq_key'), type_='unique')
    # ### end Alembic commands ###

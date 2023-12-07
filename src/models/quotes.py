from sqlalchemy import Column, Text, Integer, UniqueConstraint

from src.models.base_models import Base

class Quotes(Base):
	__tablename__ = 'quotes'

	id = Column(Integer, primary_key=True, autoincrement=True)
	quote = Column(Text, nullable=False, default="Hello, World!")
	__table_args__= (UniqueConstraint("quote", name="uniq_quote_key"),)
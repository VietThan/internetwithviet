from sqlalchemy import Column, Text, Integer, UniqueConstraint, DateTime
from sqlalchemy.sql import func

from src.models.base_models import Base

class Quotes(Base):
	__tablename__ = 'quotes'

	id = Column(Integer, primary_key=True, autoincrement=True)
	quote = Column(Text, nullable=False, default="Hello, World!")
	created_tstamp = Column(DateTime(timezone=True), nullable=True, server_default=func.now())
	modified_tstamp = Column(DateTime(timezone=True), nullable=True, onupdate=func.now())
	
	__table_args__= (UniqueConstraint("quote", name="uniq_quote_key"),)
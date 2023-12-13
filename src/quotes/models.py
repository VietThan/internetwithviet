from sqlalchemy import Column, Text, Integer, UniqueConstraint, DateTime
from sqlalchemy.sql import func
from litestar.contrib.sqlalchemy.dto import SQLAlchemyDTO

from src.models import Base

class QuotesTable(Base):
	__tablename__ = 'quotes'

	id = Column(Integer, primary_key=True, autoincrement=True)
	quote = Column(Text, nullable=False, default="Hello, World!")
	created_tstamp = Column(DateTime(timezone=True), nullable=True, server_default=func.now())
	modified_tstamp = Column(DateTime(timezone=True), nullable=True, onupdate=func.now())

	__table_args__= (UniqueConstraint("quote"),)

QuotesDTO = SQLAlchemyDTO[QuotesTable]
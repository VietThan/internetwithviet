from sqlalchemy import Column, Text, Integer, UniqueConstraint, DateTime
from sqlalchemy.sql import func
from litestar.contrib.sqlalchemy.dto import SQLAlchemyDTO
from attrs import define
from datetime import datetime

from src.models import Base, BaseDTO

from logging import getLogger
from copy import copy

LOGGER = getLogger(__name__)

class QuotesTable(Base):
	__tablename__ = 'quotes'

	id = Column(Integer, primary_key=True, autoincrement=True)
	quote = Column(Text, nullable=False, default="Hello, World!")
	created_tstamp = Column(DateTime(timezone=True), nullable=True, server_default=func.now())
	modified_tstamp = Column(DateTime(timezone=True), nullable=True, onupdate=func.now())

	__table_args__= (UniqueConstraint("quote"),)

QuotesSQLAlchemyDTO = SQLAlchemyDTO[QuotesTable]


@define
class QuotesDTO(BaseDTO):
	id: int
	quote: str
	created_tstamp: datetime
	modified_tstamp: datetime

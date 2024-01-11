from sqlalchemy import Column, Text, Integer, UniqueConstraint, DateTime
from sqlalchemy.sql import func
from litestar.contrib.sqlalchemy.dto import SQLAlchemyDTO
from attrs import define
from datetime import datetime

from src.models import Base, BaseDTO

from logging import getLogger
from copy import copy

LOGGER = getLogger(__name__)

class SourcesTable(Base):
	__tablename__ = 'sources'

	id = Column(Integer, primary_key=True, autoincrement=True)
	source_name = Column(Text, nullable=False, default="")
	source_description = Column(Text, nullable=False, default="")
	created_tstamp = Column(DateTime(timezone=True), nullable=True, server_default=func.now())
	modified_tstamp = Column(DateTime(timezone=True), nullable=True, onupdate=func.now())

	__table_args__= (UniqueConstraint("source_name"),)

SourcesSQLAlchemyDTO = SQLAlchemyDTO[SourcesTable]


@define
class SourcesDTO(BaseDTO):
	id: int
	source_name: str
	source_description: str
	created_tstamp: datetime
	modified_tstamp: datetime

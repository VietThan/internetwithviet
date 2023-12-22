from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import MetaData
from attrs import define

from logging import getLogger
from copy import copy
from typing import Any, Self

LOGGER = getLogger(__name__)

POSTGRES_INDEXES_NAMING_CONVENTION = {
    "ix": "%(column_0_label)s_idx",
    "uq": "%(table_name)s_%(column_0_name)s_uniq_key",
    "ck": "%(table_name)s_%(constraint_name)s_check",
    "fk": "%(table_name)s_%(column_0_name)s_fkey",
    "pk": "%(table_name)s_pkey",
}


# declarative base class
class Base(DeclarativeBase):
    pass

Base.metadata.naming_convention = POSTGRES_INDEXES_NAMING_CONVENTION

@define
class BaseDTO:
    @classmethod
    def from_table(cls, qt: Base) -> Self:
        d = copy(qt.__dict__)
        del d["_sa_instance_state"]
        return cls(**d)
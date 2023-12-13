from attrs import define
from litestar.dto import DataclassDTO, DTOConfig

from src.quotes.models import QuotesTable, QuotesDTO

class WriteQuotes(QuotesDTO):
    config = DTOConfig(
        exclude={
            QuotesTable.created_tstamp.name,
            QuotesTable.modified_tstamp.name,
            QuotesTable.id.name
        },
    )
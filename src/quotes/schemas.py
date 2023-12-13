from attrs import define
from litestar.dto import DataclassDTO, DTOConfig

from src.quotes.models import QuotesTable, QuotesDTO

@define
class CreateQuotePayload:
    quote: str
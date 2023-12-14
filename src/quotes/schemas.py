from attrs import define, field
from litestar.dto import DataclassDTO, DTOConfig

from src.quotes.models import QuotesTable, QuotesDTO
from src.schemas import BaseResponse

@define
class CreateQuotePayload:
    quote: str

@define
class GetAllQuotesResponse(BaseResponse):
    quotes: list[QuotesTable] = field(kw_only=True)


@define
class GetQuotesCountResponse(BaseResponse):
    count: int = field(kw_only=True)
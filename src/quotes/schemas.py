from attrs import define, field
from litestar.dto import DataclassDTO, DTOConfig

from src.quotes.models import QuotesDTO, QuotesTable, QuotesSQLAlchemyDTO
from src.schemas import BaseResponse

from typing import Generic, TypeVar
T = TypeVar("T")

@define
class CreateQuotePayload:
    quote: str

@define
class GetAllQuotesResponse(BaseResponse, Generic[T]):
    quotes: list[T] = field(kw_only=True)


@define
class GetQuotesCountResponse(BaseResponse):
    count: int = field(kw_only=True)


@define
class GetAllQuotesWebResponse(BaseResponse):
	quotes: list[QuotesDTO] = field(kw_only=True)
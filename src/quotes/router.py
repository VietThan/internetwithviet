from src.database import provide_postgres_session, provide_sqlite_session
import logging

from litestar import Request, get, post
from litestar.di import Provide
from litestar.controller import Controller
from litestar.dto import DTOData

from sqlalchemy.ext.asyncio import AsyncSession

from src.quotes.service import get_all_quotes, create_quote, get_quotes_count
from src.quotes.models import QuotesTable, QuotesSQLAlchemyDTO, QuotesDTO
from src.quotes.schemas import CreateQuotePayload, GetAllQuotesWebResponse, GetQuotesCountResponse, GetAllQuotesResponse

import logging

LOGGER = logging.getLogger(__name__)

class QuotesAPI(Controller):
    path = '/quote'
    tags = ['Quotes']

    @get('/all')
    async def get_all_quotes(self, sqlite_session: AsyncSession) -> list[QuotesTable]:
        return await get_all_quotes(sqlite_session)
    
    @get('/all-not-working')
    async def get_all_quotes_not_working(self, sqlite_session: AsyncSession) -> GetAllQuotesResponse[QuotesTable]:
        table_quotes = await get_all_quotes(sqlite_session)
        res = GetAllQuotesResponse(quotes=[QuotesDTO.from_table(t) for t in table_quotes])
        LOGGER.critical(res)
        return res
    
    @get('/all-not-working2')
    async def get_all_quotes_not_working2(self, sqlite_session: AsyncSession) -> GetAllQuotesWebResponse:
        table_quotes = await get_all_quotes(sqlite_session)
        res = GetAllQuotesWebResponse(quotes=[QuotesDTO.from_table(t) for t in table_quotes])
        LOGGER.critical(res)
        return res

    @get('/count')
    async def get_quotes_count(self, sqlite_session: AsyncSession) -> GetQuotesCountResponse:
        return GetQuotesCountResponse(count=await get_quotes_count(sqlite_session))
        

    
    @post('/')
    async def create_new_quote(self, sqlite_session: AsyncSession, data: CreateQuotePayload) -> None:
        await create_quote(sqlite_session, data.quote)
    

    
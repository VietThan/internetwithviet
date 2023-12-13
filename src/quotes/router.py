from src.database import provide_postgres_session, provide_sqlite_session
import logging

from litestar import Request, get, post
from litestar.di import Provide
from litestar.controller import Controller
from litestar.dto import DTOData

from sqlalchemy.ext.asyncio import AsyncSession

from src.quotes.service import get_all_quotes, create_quote
from src.quotes.models import QuotesTable, QuotesDTO
from src.quotes.schemas import WriteQuotes

import logging

LOGGER = logging.getLogger(__name__)

class QuotesAPI(Controller):
    path = '/quote'
    tags = ['Quotes']

    @get('/all')
    async def get_all_quotes(sqlite_session: AsyncSession) -> list[QuotesTable]:
        LOGGER.critical(f"sherlock {type(sqlite_session)}")
        return await get_all_quotes(sqlite_session)
    
    @post('/', dto=WriteQuotes)
    async def create_new_quote(sqlite_session: AsyncSession, data: QuotesTable) -> None:
        create_quote(sqlite_session, data.quote)
    

    
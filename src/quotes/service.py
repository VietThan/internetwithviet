# business logic
from sqlalchemy import select, func
from sqlalchemy.exc import IntegrityError, NoResultFound
from sqlalchemy.ext.asyncio import AsyncSession
from litestar.status_codes import HTTP_409_CONFLICT
from litestar.exceptions import HTTPException

from src.quotes.models import QuotesTable

async def get_all_quotes(sqlite_session: AsyncSession) -> list[QuotesTable]:
    query = select(QuotesTable)
    result = await sqlite_session.execute(query)
    return result.scalars().all()

async def create_quote(sqlite_session: AsyncSession, quote: str) -> None:
    new_record = QuotesTable()
    new_record.quote = quote
    sqlite_session.add(new_record)


async def get_quotes_count(sqlite_session: AsyncSession) -> int:
    result = await sqlite_session.execute(select(func.count(QuotesTable.id)))
    return result.scalar_one()
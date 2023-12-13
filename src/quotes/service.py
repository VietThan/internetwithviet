# business logic
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError, NoResultFound
from sqlalchemy.ext.asyncio import AsyncSession

from src.quotes.models import QuotesTable


async def get_all_quotes(session: AsyncSession) -> list[QuotesTable]:
    query = select(QuotesTable)
    result = await session.execute(query)
    return result.scalars().all()

async def create_quote(session: AsyncSession, quote: str) -> None:
    new_record = QuotesTable()
    new_record.quote = quote
    session.add(new_record)
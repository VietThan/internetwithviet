from litestar import Litestar, get, post, put
from litestar.contrib.sqlalchemy.plugins import SQLAlchemySerializationPlugin
from litestar.datastructures import State
from litestar.exceptions import ClientException, NotFoundException
from litestar.status_codes import HTTP_409_CONFLICT

from contextlib import asynccontextmanager
from typing import Optional
from collections.abc import AsyncGenerator

from sqlalchemy import select
from sqlalchemy.exc import IntegrityError, NoResultFound
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

from src.models import Base, Quotes

from src.configurations import Configs

app_configs = Configs()

@asynccontextmanager
async def sqlite_connection(app: Litestar) -> AsyncGenerator[None, None]:
    engine = getattr(app.state, "engine", None)
    if engine is None:
        engine = create_async_engine("sqlite+aiosqlite:///internetwithviet.db", echo=True)
        app.state.engine = engine
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    try:
        yield
    finally:
        await engine.dispose()

sessionmaker = async_sessionmaker(expire_on_commit=False)


async def provide_sqlite_session(state: State) -> AsyncGenerator[AsyncSession, None]:
    async with sessionmaker(bind=state.engine) as session:
        try:
            async with session.begin():
                yield session
        except IntegrityError as exc:
            raise ClientException(
                status_code=HTTP_409_CONFLICT,
                detail=str(exc),
            ) from exc

@get("/")
async def hello_world() -> dict[str, str]:
    """Handler function that returns a greeting dictionary."""
    return {"hello": "world"}

@get("/ping")
async def ping() -> dict[str, str]:
    """Handler function that returns a greeting dictionary."""
    return {"hello": "world"}

async def get_all_quotes(session: AsyncSession) -> list[Quotes]:
    query = select(Quotes)
    result = await session.execute(query)
    return result.scalars().all()

@get("/quotes")
async def get_quotes(sqlite_session: AsyncSession) -> list[Quotes]:
    return await get_all_quotes(sqlite_session)


app = Litestar(
    [hello_world, ping, get_quotes],
    dependencies={"sqlite_session": provide_sqlite_session}, # DI into
    lifespan=[sqlite_connection], # connection lasts lifespan of application
    plugins=[SQLAlchemySerializationPlugin()],
)
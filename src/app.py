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

from src.configurations import Configs, make_postgres_url

app_configs = Configs()

@asynccontextmanager
async def sqlite_connection(app: Litestar) -> AsyncGenerator[None, None]:
    sqlite_engine = getattr(app.state, "sqlite_engine", None)
    if sqlite_engine is None:
        sqlite_engine = create_async_engine("sqlite+aiosqlite:///internetwithviet.db", echo=True)
        app.state.sqlite_engine = sqlite_engine
    async with sqlite_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    try:
        yield
    finally:
        await sqlite_engine.dispose()

@asynccontextmanager
async def postgres_connection(app: Litestar) -> AsyncGenerator[None, None]:
    postgres_engine = getattr(app.state, "postgres_engine", None)
    if postgres_engine is None:
        postgres_engine = create_async_engine(make_postgres_url(), echo=True)
        app.state.postgres_engine = postgres_engine
    async with postgres_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    try:
        yield
    finally:
        await postgres_engine.dispose()

sessionmaker = async_sessionmaker(expire_on_commit=False)


async def provide_sqlite_session(state: State) -> AsyncGenerator[AsyncSession, None]:
    async with sessionmaker(bind=state.sqlite_engine) as sqlite_session:
        try:
            async with sqlite_session.begin():
                yield sqlite_session
        except IntegrityError as exc:
            raise ClientException(
                status_code=HTTP_409_CONFLICT,
                detail=str(exc),
            ) from exc
        
async def provide_postgres_session(state: State) -> AsyncGenerator[AsyncSession, None]:
    async with sessionmaker(bind=state.postgres_engine) as postgres_session:
        try:
            async with postgres_session.begin():
                yield postgres_session
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
    dependencies={
        "sqlite_session": provide_sqlite_session,
        "postgres_session": provide_postgres_session
    }, # DI into
    lifespan=[sqlite_connection, postgres_connection], # connection lasts lifespan of application
    plugins=[SQLAlchemySerializationPlugin()],
)
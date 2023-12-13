from configurations import make_postgres_url
from litestar.datastructures import State
from litestar.exceptions import ClientException
from litestar.status_codes import HTTP_409_CONFLICT
from sqlalchemy.exc import IntegrityError
from src import Base


from litestar import Litestar
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine


from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager


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
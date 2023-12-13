from database import postgres_connection, provide_postgres_session, provide_sqlite_session, sqlite_connection
from litestar import Litestar, get, Router
from litestar.contrib.sqlalchemy.plugins import SQLAlchemySerializationPlugin
from litestar.response import File
from litestar.openapi import OpenAPIConfig
from litestar.openapi.spec import Tag

import pathlib

from src.configurations import Configs
from src.quotes.router import QuotesAPI

# initializing configs
app_configs = Configs()

@get("/", summary="Handler function that returns a greeting dictionary.")
async def hello_world() -> dict[str, str]:
    """Handler function that returns a greeting dictionary."""
    return {"hello": "world"}

@get("/ping", summary="Ping!")
async def ping() -> dict[str, str]:
    return {"hello": "world"}

@get('/favicon.ico', summary="Returns favicon requested by browser" )
async def favicon() -> File:
    path = pathlib.Path(__file__).parent / "static/crylaugh2.ico"
    return File(
        path=path,
        filename="favicon.ico"
    )

api_router = Router(
    path="/api", 
    route_handlers=[QuotesAPI],   
)

from litestar.di import Provide

app = Litestar(
    [hello_world, ping, favicon, api_router],
    openapi_config=OpenAPIConfig(
        title="Internet With Viet Backend",
        version='0.1',
        tags=[
            Tag(name="Quotes", description="Routes to interact with Quotes data")
        ],
    ),
    dependencies={
        "sqlite_session": provide_sqlite_session,
        "postgres_session": provide_postgres_session
    }, # DI into  
    lifespan=[sqlite_connection, postgres_connection], # connection lasts lifespan of application
    plugins=[SQLAlchemySerializationPlugin()],
)
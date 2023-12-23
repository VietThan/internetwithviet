from database import postgres_connection, provide_postgres_session, provide_sqlite_session, sqlite_connection
from litestar import Litestar, get, Router
from litestar.contrib.sqlalchemy.plugins import SQLAlchemySerializationPlugin
from litestar.response import File
from litestar.openapi import OpenAPIConfig
from litestar.openapi.spec import Tag
from litestar.contrib.jinja import JinjaTemplateEngine
from litestar.response import Template
from litestar.template.config import TemplateConfig

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

@get(path="/{name: str}/{template_type: str}", sync_to_thread=False)
def index(name: str, template_type: str) -> Template:
    if template_type == "file":
        return Template(template_name="hello.html.jinja2", context={"name": name})
    elif template_type == "string":
        return Template(template_str="Hello <strong>Jinja</strong> using strings with name: {{ name }}", context={"name": name})

from litestar.di import Provide

app = Litestar(
    [hello_world, ping, favicon, index, api_router],
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
    template_config=TemplateConfig(
        directory=pathlib.Path(__file__).parent / "templates",
        engine=JinjaTemplateEngine,
    ),
)
from sanic.request import Request
from sanic.response import text


async def ping(_: Request):
    return text("pong")

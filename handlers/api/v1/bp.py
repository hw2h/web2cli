from sanic import Blueprint
from .handlers import CMDHandler, LSHandler
from .system import ping

bp = Blueprint("api", url_prefix="/api/v1")

# commands:
bp.add_route(CMDHandler.as_view(), "/cmd")
bp.add_route(LSHandler.as_view(), "/ls")

# system:
bp.add_route(ping, "/ping")

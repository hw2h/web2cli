import asyncio
import logging

from sanic import Sanic, json, Request
from sanic.handlers import ErrorHandler
from sanic.log import LOGGING_CONFIG_DEFAULTS

from handlers.api.v1.bp import bp
from handlers.api.v1.handlers import ApiError


logger = logging.getLogger(__name__)


class ApiErrorsHandler(ErrorHandler):
    def default(self, request, exception):
        if isinstance(exception, ApiError):
            return json(
                exception.as_dict(),
                status=exception.status_code,
                headers={"Content-Type": "application/json"}
            )
        else:
            return super().default(request, exception)


def register_errors(app):
    @app.exception(ApiError)
    def _api_error_exception(request: Request, exception: ApiError):
        logger.exception("request=%s error: %s %s", request, exception, request.body)
        return json(exception.as_dict(), status=exception.status_code)


async def shutdown(app):
    logger.warning("Server soon will stops, unfinished tasks:")
    for task in asyncio.all_tasks():
        logger.warning(f"{task}\n")


def create_app():
    application = Sanic(
        "WebCLI",
        error_handler=ApiErrorsHandler(),
        log_config=LOGGING_CONFIG_DEFAULTS,
    )
    register_errors(application)

    application.blueprint(bp)
    application.register_listener(shutdown, "before_server_stop")
    return application


if __name__ == "__main__":
    app = create_app()
    app.run(
        debug=False,
        host='0.0.0.0',
        port=8008,
        access_log=False,
    )

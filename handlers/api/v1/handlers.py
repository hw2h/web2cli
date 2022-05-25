import asyncio
from http import HTTPStatus

from sanic.views import HTTPMethodView
from sanic.response import json
from marshmallow.exceptions import ValidationError

from .schemas import ExecCMDSchema, LSSchema
from lib.cli_ops import exec_cmd, exec_ls, NotAllowedCMD


class ApiError(Exception):
    def __init__(self, errors, status_code: int):
        self.result = errors
        self.status_code = status_code

    def as_dict(self):
        return {
            "message": self.result,
            "status": self.status_code
        }


class CMDHandler(HTTPMethodView):
    """Run arbitrary command"""
    @staticmethod
    async def post(request):
        try:
            data = ExecCMDSchema().loads(request.body.decode())
            stdout, stderr = await exec_cmd(data["command"], data["arg"], data.get("opts"))
        except ValidationError as e:
            raise ApiError(e.messages, status_code=HTTPStatus.BAD_REQUEST)
        except asyncio.TimeoutError:
            raise ApiError(
                "Timeout error. Command executed too long",
                status_code=HTTPStatus.GATEWAY_TIMEOUT,
            )
        except NotAllowedCMD as e:
            raise ApiError(
                f"Command {e} is not allowed",
                status_code=HTTPStatus.NOT_IMPLEMENTED,
            )
        if stderr:
            raise ApiError(stderr.decode(), status_code=HTTPStatus.INTERNAL_SERVER_ERROR)
        return json({
            "response": stdout.decode(),
        })


class LSHandler(HTTPMethodView):
    """
        List directory contents
        Run `ls` command with operands and options: `ls [-ABCFGHLOPRSTUW@abcdefghiklmnopqrstuwx1%] [file ...]`
        Optional params:
            operands: file ...
            available options: ABCFGHLOPRSTUW@abcdefghiklmnopqrstuwx1%

        see `man ls`
    """
    async def post(self, request):
        try:
            data = LSSchema().loads(request.body.decode())
            stdout, stderr = await exec_ls(data["operands"], data["options"])
        except ValidationError as e:
            raise ApiError(e.messages, status_code=HTTPStatus.BAD_REQUEST)
        except asyncio.TimeoutError:
            raise ApiError(
                "Timeout error. Command executed too long",
                status_code=HTTPStatus.GATEWAY_TIMEOUT,
            )
        except Exception as e:
            raise ApiError(
                f"ls command exception {e}",
                status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
            )
        self._handle_errors(stderr)
        return json({
            "response": stdout.decode(),
        })

    @staticmethod
    def _handle_errors(stderr: bytes):
        if not stderr:
            return None
        err = stderr.decode()
        if "No such file" in err:
            raise ApiError(
                f"Wrong path: {err}",
                status_code=HTTPStatus.NOT_FOUND
            )
        if "Permission denied" in err:
            raise ApiError(
                f"Wrong path: {err}",
                status_code=HTTPStatus.FORBIDDEN
            )

import asyncio
import shlex
from typing import Tuple, Optional


DEFAULT_TIMEOUT = 10.0
ALLOWED_COMMANDS = {"ls", "ping", "cat", "head", "tail", "ifconfig"}


class NotAllowedCMD(Exception):
    pass


def make_cmd(command: str, arg: str, opts: Optional[str]) -> str:
    if not opts:
        return shlex.join([command, arg])
    return shlex.join(
        [command, *shlex.split(opts), arg]
    )


async def call_cmd(cmd: str) -> Tuple[bytes, bytes]:
    proc = await asyncio.create_subprocess_shell(
        cmd,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
    )
    return await proc.communicate()


async def exec_cmd(
        command: str,
        arg: str,
        opts: Optional[str] = None,
        *,
        timeout=DEFAULT_TIMEOUT
) -> Tuple[bytes, bytes]:
    if command.lower() not in ALLOWED_COMMANDS:
        raise NotAllowedCMD(command)
    cmd = make_cmd(command, arg, opts)
    task = asyncio.wait_for(call_cmd(cmd), timeout=timeout)
    stdout, stderr = await task
    return stdout, stderr


async def exec_ls(
        operands: Optional[str] = None,
        options: Optional[str] = None,
        *,
        timeout=DEFAULT_TIMEOUT,
) -> Tuple[bytes, bytes]:
    if options and not options.startswith("-"):
        options = f"-{options}"
    cmd = make_cmd("ls", operands, options)
    task = asyncio.wait_for(call_cmd(cmd), timeout=timeout)
    stdout, stderr = await task
    return stdout, stderr

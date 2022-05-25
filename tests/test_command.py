import pytest

from lib.cli_ops import exec_cmd


pytestmark = pytest.mark.asyncio


async def test_ls_app_dir():
    command, arg = "ls", "./tests"
    stdout, stderr = await exec_cmd(command, arg)
    assert stderr == b""
    stdout_files = stdout.decode().split("\n")
    assert "test_command.py" in stdout_files

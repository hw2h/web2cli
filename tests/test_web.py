import ujson
import pytest


@pytest.mark.asyncio
async def test_ping(app):
    request, response = await app.asgi_client.get("/api/v1/ping/")
    assert response.body == b"pong"
    assert response.status == 200


@pytest.mark.asyncio
async def test_cmd(app):
    request, response = await app.asgi_client.post(
        "/api/v1/cmd/",
        json={
            "command": "ls",
            "arg": "./tests"
        }
    )
    assert response.status == 200
    data = ujson.loads(response.body)
    for f in ("conftest.py", "test_command.py", "test_web.py"):
        assert f in data["response"]

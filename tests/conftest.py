import pytest

from app.server import create_app


@pytest.fixture
def event_loop(loop):
    return loop


@pytest.fixture
def app():
    application = create_app()
    return application

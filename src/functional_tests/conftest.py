import os
import pytest


@pytest.fixture(scope="session", autouse=True)
def set_env():
    os.environ["DJANGO_ALLOW_ASYNC_UNSAFE"] = "1"


@pytest.fixture
def live_server_url(live_server):
    if test_server := os.environ.get("TEST_SERVER"):
        return "http://" + test_server
    return live_server.url

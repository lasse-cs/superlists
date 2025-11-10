import os
import pytest

from django.conf import settings
from django.contrib.auth import get_user_model

from .container_commands import create_session_on_server, reset_database
from .management.commands.create_session import create_pre_authenticated_session


User = get_user_model()


@pytest.fixture(scope="session", autouse=True)
def set_env():
    os.environ["DJANGO_ALLOW_ASYNC_UNSAFE"] = "1"


@pytest.fixture(scope="session")
def test_server():
    return os.environ.get("TEST_SERVER")


@pytest.fixture(scope="session")
def test_email():
    return os.environ.get("TEST_EMAIL", "edith@example.com")


@pytest.fixture
def live_server_url(test_server, live_server):
    if test_server:
        reset_database(test_server)
        return "http://" + test_server
    return live_server.url


@pytest.fixture
def pre_authenticated_session(live_server_url: str, test_server: str):
    def _pre_authenticated_session(email, page):
        if test_server:
            session_key = create_session_on_server(test_server, email)
        else:
            session_key = create_pre_authenticated_session(email)

        ## to set a cookie we need to first visit the domain
        ## 404 pages load the quickest
        page.goto(live_server_url + "/404_no_such_url/")
        page.context.add_cookies(
            [
                {
                    "name": settings.SESSION_COOKIE_NAME,
                    "value": session_key,
                    "url": live_server_url,
                },
            ],
        )

    return _pre_authenticated_session

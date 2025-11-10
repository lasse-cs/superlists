import os
import pytest

from django.conf import settings
from django.contrib.auth import BACKEND_SESSION_KEY, SESSION_KEY, get_user_model
from django.contrib.sessions.backends.db import SessionStore


User = get_user_model()


@pytest.fixture(scope="session", autouse=True)
def set_env():
    os.environ["DJANGO_ALLOW_ASYNC_UNSAFE"] = "1"


@pytest.fixture
def live_server_url(live_server):
    if test_server := os.environ.get("TEST_SERVER"):
        return "http://" + test_server
    return live_server.url


@pytest.fixture
def pre_authenticated_session():
    def _pre_authenticated_session(email, live_server_url, page):
        user = User.objects.create(email=email)
        session = SessionStore()
        session[SESSION_KEY] = user.pk
        session[BACKEND_SESSION_KEY] = settings.AUTHENTICATION_BACKENDS[0]
        session.save()

        ## to set a cookie we need to first visit the domain
        ## 404 pages load the quickest
        page.goto(live_server_url + "/404_no_such_url/")
        page.context.add_cookies(
            [
                {
                    "name": settings.SESSION_COOKIE_NAME,
                    "value": session.session_key,
                    "url": live_server_url,
                },
            ],
        )

    return _pre_authenticated_session

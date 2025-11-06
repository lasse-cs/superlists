import os
import pytest


@pytest.fixture(scope="session", autouse=True)
def set_env():
    os.environ["DJANGO_ALLOW_ASYNC_UNSAFE"] = "1"

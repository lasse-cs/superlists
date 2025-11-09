import pytest

from django.http import HttpRequest

from accounts.authentication import PasswordlessAuthenticationBackend
from accounts.models import Token, User


pytestmark = pytest.mark.django_db


def test_authenticate_returns_none_if_no_such_token():
    result = PasswordlessAuthenticationBackend().authenticate(
        HttpRequest(), "no-such-token",
    )
    assert result is None


def test_authenticate_returns_new_user_with_correct_email_if_token_exists():
    email = "edith@example.com"
    token = Token.objects.create(email=email)
    user = PasswordlessAuthenticationBackend().authenticate(
        HttpRequest(), token.uid 
    )
    new_user = User.objects.get(email=email)
    assert user == new_user


def test_authenticate_returns_existing_user_with_correct_email_if_token_exists():
    email = "edith@example.com"
    existing_user = User.objects.create(email=email)
    token = Token.objects.create(email=email)
    user = PasswordlessAuthenticationBackend().authenticate(
        HttpRequest(), token.uid
    )
    assert user == existing_user


def test_get_user_by_email():
    User.objects.create(email="another@example.com")
    desired_user = User.objects.create(email="edith@example.com")
    found_user = PasswordlessAuthenticationBackend().get_user("edith@example.com")
    assert found_user == desired_user

def test_get_user_returns_None_if_no_user_with_that_email():
    assert PasswordlessAuthenticationBackend().get_user("edith@example.com") is None

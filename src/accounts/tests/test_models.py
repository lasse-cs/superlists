import pytest

from django.contrib import auth

from accounts.models import User


pytestmark = pytest.mark.django_db


def test_model_is_configured_for_django_auth():
    assert auth.get_user_model() == User


def test_user_is_valid_with_email_only():
    user = User(email="a@b.com")
    user.full_clean()  # should not raise


def test_email_is_primary_key():
    user = User(email="a@b.com")
    assert user.pk == "a@b.com"

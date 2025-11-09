import pytest

from unittest import mock

from pytest_django.asserts import assertRedirects

from django.contrib import auth

from accounts.models import Token
import accounts.views


pytestmark = pytest.mark.django_db


def test_send_login_email_redirects_to_home_page(client):
    response = client.post(
        "/accounts/send_login_email", data={"email": "edith@example.com"}
    )
    assertRedirects(response, "/")


@mock.patch("accounts.views.send_mail")
def test_sends_mail_to_address_from_post(mock_send_mail, client, settings):
    client.post("/accounts/send_login_email", data={"email": "edith@example.com"})

    assert mock_send_mail.called
    (subject, _, from_email, to_list), _ = mock_send_mail.call_args
    assert subject == "Your login link for Superlists"
    assert from_email == settings.DEFAULT_FROM_EMAIL
    assert to_list == ["edith@example.com"]


def test_add_success_message(client):
    response = client.post(
        "/accounts/send_login_email",
        data={"email": "edith@example.com"},
        follow=True,
    )

    message = list(response.context["messages"])[0]
    assert (
        message.message
        == "Check your email, we've sent you a link you can use to log in."
    )
    assert message.tags == "success"


def test_creates_token_with_associated_email(client):
    client.post("/accounts/send_login_email", data={"email": "edith@example.com"})

    token = Token.objects.get()
    assert token.email == "edith@example.com"


@mock.patch("accounts.views.send_mail")
def test_sends_link_to_login_using_token_uid(mock_send_mail, client, settings):
    client.post("/accounts/send_login_email", data={"email": "edith@example.com"})
    token = Token.objects.get()
    expected_url = f"http://testserver/accounts/login?token={token.uid}"
    (_, body, _, _), _ = mock_send_mail.call_args
    assert expected_url in body


def test_login_token_redirects_to_home_page(client):
    response = client.get("/accounts/login?token=abcd123")
    assertRedirects(response, "/")


def test_logs_in_if_given_valid_token(client):
    anon_user = auth.get_user(client)
    assert not anon_user.is_authenticated

    token = Token.objects.create(email="edith@example.com")
    client.get(f"/accounts/login?token={token.uid}")

    user = auth.get_user(client)
    assert user.is_authenticated
    assert user.email == "edith@example.com"


def test_shows_login_error_if_token_invalid(client):
    response = client.get("/accounts/login?token=invalid-token", follow=True)

    user = auth.get_user(client)
    assert not user.is_authenticated

    message = list(response.context["messages"])[0]
    assert message.message == "Invalid login link, please request a new one"
    assert message.tags == "error"


@mock.patch("accounts.views.auth")
def test_calls_authenticate_with_uid_from_get_request(mock_auth, client):
    client.get("/accounts/login?token=abcd123")
    assert mock_auth.authenticate.call_args == mock.call(uid="abcd123")

import re
import pytest

from django.core import mail

from playwright.sync_api import expect, Page

TEST_EMAIL = "edith@example.com"
SUBJECT = "Your login link for Superlists"


def test_login_using_magic_link(live_server_url: str, page: Page):
    # Edith goes to the awesome superlists site
    # and notices a "Log in" section in the navbar for the first time
    # It's telling her to enter her email address, so she does
    page.goto(live_server_url)
    loginbox = page.locator("input[name=email]")
    loginbox.fill(TEST_EMAIL)
    loginbox.press("Enter")

    body = page.locator("body")
    expect(body).to_have_text(re.compile("Check your email"))

    # She checks her email and finds a message
    email = mail.outbox.pop()
    assert TEST_EMAIL in email.to
    assert email.subject == SUBJECT

    # It has a URL link in it
    assert "Use this link to log in" in email.body
    url_search = re.search(r"http://.+/.+$", email.body)
    if not url_search:
        pytest.fail(f"Could not find url in email body:\n{email.body}")
    url = url_search.group(0)
    assert live_server_url in url

    # she clicks it
    page.goto(url)

    # she is logged in
    expect(page.locator("#id_logout")).to_be_visible()
    expect(page.locator(".navbar")).to_have_text(re.compile(TEST_EMAIL))

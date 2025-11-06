from django.http import HttpRequest
from pytest_django.asserts import assertContains, assertTemplateUsed

from lists.views import home_page


def test_home_page_returns_correct_html(client):
    response = client.get("/")
    assertTemplateUsed(response, "home.html")


def test_renders_homepage_content(client):
    response = client.get("/")
    assertContains(response, "To-Do")

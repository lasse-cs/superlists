from django.http import HttpRequest
from pytest_django.asserts import assertContains 

from lists.views import home_page


def test_home_page_returns_correct_html(client):
    response = client.get("/")
    assertContains(response, "<title>To-Do lists</title>")
    assertContains(response, "<html>")
    assertContains(response, "</html>")

from django.http import HttpRequest
from pytest_django.asserts import assertContains, assertTemplateUsed

from lists.views import home_page


def test_uses_home_template(client):
    response = client.get("/")
    assertTemplateUsed(response, "home.html")


def test_renders_input_form(client):
    response = client.get("/")
    assertContains(response, '<form method="POST">')
    assertContains(response, '<input name="item_text"')


def test_can_save_a_POST_request(client):
    response = client.post("/", data={"item_text": "A new list item"})
    assertContains(response, "A new list item")
    assertTemplateUsed(response, "home.html")

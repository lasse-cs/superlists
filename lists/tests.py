import pytest

from django.http import HttpRequest
from pytest_django.asserts import assertContains, assertTemplateUsed

from lists.models import Item
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


@pytest.mark.django_db
def test_saving_and_retrieving_items():
    first_item = Item()
    first_item.text = "The first (ever) list item"
    first_item.save()

    second_item = Item()
    second_item.text = "Item the second"
    second_item.save()

    saved_items = Item.objects.all()
    assert saved_items.count() == 2

    first_saved_item = saved_items[0]
    second_saved_item = saved_items[1]

    assert first_saved_item.text == "The first (ever) list item"
    assert second_saved_item.text == "Item the second"

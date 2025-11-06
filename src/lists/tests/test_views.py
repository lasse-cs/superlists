import lxml.html
import pytest

from django.http import HttpRequest
from django.utils import html

from pytest_django.asserts import (
    assertContains,
    assertNotContains,
    assertRedirects,
    assertTemplateUsed,
)

from lists.models import Item, List
from lists.views import home_page


pytestmark = pytest.mark.django_db


def test_home_page_uses_home_template(client):
    response = client.get("/")
    assertTemplateUsed(response, "home.html")


def test_home_page_renders_input_form(client):
    response = client.get("/")
    parsed = lxml.html.fromstring(response.content)
    [form] = parsed.cssselect("form[method=POST]")
    assert form.get("action") == "/lists/new"
    inputs = form.cssselect("input")
    assert "item_text" in [input.get("name") for input in inputs]


def test_new_list_can_save_a_POST_request(client):
    response = client.post("/lists/new", data={"item_text": "A new list item"})

    assert Item.objects.count() == 1
    new_item = Item.objects.first()
    assert new_item.text == "A new list item"


def test_new_list_redirects_after_POST(client):
    response = client.post("/lists/new", data={"item_text": "A new list item"})
    new_list = List.objects.get()
    assertRedirects(response, f"/lists/{new_list.id}/")


def test_new_item_can_save_a_POST_request_to_an_existing_list(client):
    List.objects.create()
    correct_list = List.objects.create()

    client.post(
        f"/lists/{correct_list.id}/add_item",
        data={"item_text": "A new item for an existing list"},
    )

    assert Item.objects.count() == 1

    new_item = Item.objects.get()
    assert new_item.text == "A new item for an existing list"
    assert new_item.list == correct_list


def test_new_item_redirects_to_list_view(client):
    List.objects.create()
    correct_list = List.objects.create()

    response = client.post(
        f"/lists/{correct_list.id}/add_item",
        data={"item_text": "A new item for an existing list"},
    )
    assertRedirects(response, f"/lists/{correct_list.id}/")


def test_new_item_validation_errors_are_sent_back_to_home_page_template(client):
    response = client.post("/lists/new", data={"item_text": ""})
    assert response.status_code == 200
    assertTemplateUsed(response, "home.html")
    expected_error = html.escape("You can't have an empty list item")
    assertContains(response, expected_error)


def test_new_item_invalid_list_items_arent_saved(client):
    client.post("/lists/new", data={"item_text": ""})
    assert List.objects.count() == 0
    assert Item.objects.count() == 0


def test_list_view_uses_list_template(client):
    mylist = List.objects.create()
    reponse = client.get(f"/lists/{mylist.id}/")
    assertTemplateUsed(reponse, "list.html")


def test_list_view_renders_input_form(client):
    mylist = List.objects.create()
    response = client.get(f"/lists/{mylist.id}/")
    parsed = lxml.html.fromstring(response.content)
    [form] = parsed.cssselect("form[method=POST]")
    assert form.get("action") == f"/lists/{mylist.id}/add_item"
    inputs = form.cssselect("input")
    assert "item_text" in [input.get("name") for input in inputs]


def test_list_view_displays_only_items_for_that_list(client):
    correct_list = List.objects.create()
    Item.objects.create(text="itemey 1", list=correct_list)
    Item.objects.create(text="itemey 2", list=correct_list)

    other_list = List.objects.create()
    Item.objects.create(text="other list item", list=other_list)

    response = client.get(f"/lists/{correct_list.id}/")

    assertContains(response, "itemey 1")
    assertContains(response, "itemey 2")
    assertNotContains(response, "other list item")

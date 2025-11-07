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

from lists.forms import EMPTY_ITEM_ERROR
from lists.models import Item, List
from lists.views import home_page


pytestmark = pytest.mark.django_db


@pytest.fixture
def invalid_new_list_input_response(client):
    return client.post("/lists/new", data={"text": ""})


@pytest.fixture
def invalid_new_item_input_response(client):
    mylist = List.objects.create()
    return client.post(f"/lists/{mylist.id}/", data={"text": ""})

def test_home_page_uses_home_template(client):
    response = client.get("/")
    assertTemplateUsed(response, "home.html")


def test_home_page_renders_input_form(client):
    response = client.get("/")
    parsed = lxml.html.fromstring(response.content)
    [form] = parsed.cssselect("form[method=POST]")
    assert form.get("action") == "/lists/new"
    inputs = form.cssselect("input")
    assert "text" in [input.get("name") for input in inputs]


def test_new_list_can_save_a_POST_request(client):
    response = client.post("/lists/new", data={"text": "A new list item"})

    assert Item.objects.count() == 1
    new_item = Item.objects.first()
    assert new_item.text == "A new list item"


def test_new_list_redirects_after_POST(client):
    response = client.post("/lists/new", data={"text": "A new list item"})
    new_list = List.objects.get()
    assertRedirects(response, f"/lists/{new_list.id}/")


def test_new_list_invalid_input_nothing_saved_to_db(invalid_new_list_input_response):
    assert Item.objects.count() == 0


def test_new_list_invalid_input_renders_home_template(invalid_new_list_input_response):
    assert invalid_new_list_input_response.status_code == 200
    assertTemplateUsed(invalid_new_list_input_response, "home.html")


def test_new_list_invalid_input_shows_error_on_page(invalid_new_list_input_response):
    assertContains(invalid_new_list_input_response, html.escape(EMPTY_ITEM_ERROR))


def test_list_view_uses_list_template(client):
    mylist = List.objects.create()
    response = client.get(f"/lists/{mylist.id}/")
    assertTemplateUsed(response, "list.html")


def test_list_view_renders_input_form(client):
    mylist = List.objects.create()
    response = client.get(f"/lists/{mylist.id}/")
    parsed = lxml.html.fromstring(response.content)
    [form] = parsed.cssselect("form[method=POST]")
    assert form.get("action") == f"/lists/{mylist.id}/"
    inputs = form.cssselect("input")
    assert "text" in [input.get("name") for input in inputs]


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


def test_list_view_can_save_a_POST_request_to_an_existing_list(client):
    List.objects.create()
    correct_list = List.objects.create()

    client.post(
        f"/lists/{correct_list.id}/",
        data={"text": "A new item for an existing list"},
    )

    assert Item.objects.count() == 1

    new_item = Item.objects.get()
    assert new_item.text == "A new item for an existing list"
    assert new_item.list == correct_list


def test_list_view_POST_redirects_to_list_view(client):
    List.objects.create()
    correct_list = List.objects.create()

    response = client.post(
        f"/lists/{correct_list.id}/",
        data={"text": "A new item for an existing list"},
    )
    assertRedirects(response, f"/lists/{correct_list.id}/")

def test_list_view_invalid_input_nothing_saved_to_db(invalid_new_item_input_response):
    assert Item.objects.count() == 0

def test_list_view_invalid_input_renders_list_template(invalid_new_item_input_response):
    assert invalid_new_item_input_response.status_code == 200
    assertTemplateUsed(invalid_new_item_input_response, "list.html")

def test_list_view_invalid_input_shows_error_on_page(invalid_new_item_input_response):
    assertContains(invalid_new_item_input_response, html.escape(EMPTY_ITEM_ERROR))

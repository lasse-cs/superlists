import lxml.html
import pytest

from django.utils import html

from pytest_django.asserts import (
    assertContains,
    assertNotContains,
    assertRedirects,
    assertTemplateUsed,
)

from lists.forms import DUPLICATE_ITEM_ERROR, EMPTY_ITEM_ERROR
from lists.models import Item, List


pytestmark = pytest.mark.django_db


@pytest.fixture
def invalid_response(client):
    mylist = List.objects.create()
    return client.post(f"/lists/{mylist.id}/", data={"text": ""})


def test_uses_list_template(client):
    mylist = List.objects.create()
    response = client.get(f"/lists/{mylist.id}/")
    assertTemplateUsed(response, "list.html")


def test_renders_input_form(client):
    mylist = List.objects.create()
    response = client.get(f"/lists/{mylist.id}/")
    parsed = lxml.html.fromstring(response.content)
    forms = parsed.cssselect("form[method=POST]")
    url = f"/lists/{mylist.id}/"
    assert url in [form.get("action") for form in forms]
    [form] = [form for form in forms if form.get("action") == url]
    inputs = form.cssselect("input")
    assert "text" in [input.get("name") for input in inputs]


def test_displays_only_items_for_that_list(client):
    correct_list = List.objects.create()
    Item.objects.create(text="itemey 1", list=correct_list)
    Item.objects.create(text="itemey 2", list=correct_list)

    other_list = List.objects.create()
    Item.objects.create(text="other list item", list=other_list)

    response = client.get(f"/lists/{correct_list.id}/")

    assertContains(response, "itemey 1")
    assertContains(response, "itemey 2")
    assertNotContains(response, "other list item")


def test_can_save_a_POST_request_to_an_existing_list(client):
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


def test_POST_redirects_to_list_view(client):
    List.objects.create()
    correct_list = List.objects.create()

    response = client.post(
        f"/lists/{correct_list.id}/",
        data={"text": "A new item for an existing list"},
    )
    assertRedirects(response, f"/lists/{correct_list.id}/")


def test_invalid_input_nothing_saved_to_db(invalid_response):
    assert Item.objects.count() == 0


def test_invalid_input_renders_list_template(invalid_response):
    assert invalid_response.status_code == 200
    assertTemplateUsed(invalid_response, "list.html")


def test_invalid_input_shows_error_on_page(invalid_response):
    assertContains(invalid_response, html.escape(EMPTY_ITEM_ERROR))


def test_duplicate_item_validation_errors_end_up_on_lists_page(client):
    list1 = List.objects.create()
    Item.objects.create(list=list1, text="textey")

    response = client.post(
        f"/lists/{list1.id}/",
        data={"text": "textey"},
    )

    expected_error = html.escape(DUPLICATE_ITEM_ERROR)
    assertContains(response, expected_error)
    assertTemplateUsed(response, "list.html")
    assert Item.objects.count() == 1


def test_for_invalid_input_sets_is_invalid_class(invalid_response):
    parsed = lxml.html.fromstring(invalid_response.content)
    [input] = parsed.cssselect("input[name=text]")
    assert "is-invalid" in set(input.classes)

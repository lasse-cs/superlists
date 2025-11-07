import pytest

from django.utils import html

from pytest_django.asserts import (
    assertContains,
    assertRedirects,
    assertTemplateUsed,
)

from lists.forms import EMPTY_ITEM_ERROR
from lists.models import Item, List


pytestmark = pytest.mark.django_db


@pytest.fixture
def invalid_response(client):
    return client.post("/lists/new", data={"text": ""})


def test_can_save_a_POST_request(client):
    response = client.post("/lists/new", data={"text": "A new list item"})

    assert Item.objects.count() == 1
    new_item = Item.objects.first()
    assert new_item.text == "A new list item"


def test_redirects_after_POST(client):
    response = client.post("/lists/new", data={"text": "A new list item"})
    new_list = List.objects.get()
    assertRedirects(response, f"/lists/{new_list.id}/")


def test_invalid_input_nothing_saved_to_db(invalid_response):
    assert Item.objects.count() == 0


def test_invalid_input_renders_home_template(invalid_response):
    assert invalid_response.status_code == 200
    assertTemplateUsed(invalid_response, "home.html")


def test_invalid_input_shows_error_on_page(invalid_response):
    assertContains(invalid_response, html.escape(EMPTY_ITEM_ERROR))

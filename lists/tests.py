import pytest

from django.http import HttpRequest
from pytest_django.asserts import assertContains, assertRedirects, assertTemplateUsed

from lists.models import Item
from lists.views import home_page


pytestmark = pytest.mark.django_db


def test_home_page_uses_home_template(client):
    response = client.get("/")
    assertTemplateUsed(response, "home.html")


def test_home_page_renders_input_form(client):
    response = client.get("/")
    assertContains(response, '<form method="POST" action="/">')
    assertContains(response, '<input name="item_text"')


def test_new_list_can_save_a_POST_request(client):
    response = client.post("/lists/new", data={"item_text": "A new list item"})

    assert Item.objects.count() == 1
    new_item = Item.objects.first()
    assert new_item.text == "A new list item"


def test_new_list_redirects_after_POST(client):
    response = client.post("/lists/new", data={"item_text": "A new list item"})
    assertRedirects(response, "/lists/the-only-list-in-the-world/")


def test_list_view_uses_list_template(client):
    reponse = client.get("/lists/the-only-list-in-the-world/")
    assertTemplateUsed(reponse, "list.html")


def test_list_view_renders_input_form(client):
    response = client.get("/lists/the-only-list-in-the-world/")
    assertContains(response, '<form method="POST" action="/">')
    assertContains(response, '<input name="item_text"')


def test_list_view_displays_all_list_items(client):
    Item.objects.create(text="itemey 1")
    Item.objects.create(text="itemey 2")

    response = client.get("/lists/the-only-list-in-the-world/")

    assertContains(response, "itemey 1")
    assertContains(response, "itemey 2")


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

import pytest

from django.http import HttpRequest
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
    assertContains(response, '<form method="POST" action="/lists/new">')
    assertContains(
        response,
        '<input name="item_text" id="id_new_item" placeholder="Enter a to-do item" />',
        html=True,
    )


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


def test_list_view_uses_list_template(client):
    mylist = List.objects.create()
    reponse = client.get(f"/lists/{mylist.id}/")
    assertTemplateUsed(reponse, "list.html")


def test_list_view_renders_input_form(client):
    mylist = List.objects.create()
    response = client.get(f"/lists/{mylist.id}/")
    assertContains(
        response, f'<form method="POST" action="/lists/{mylist.id}/add_item">'
    )
    assertContains(
        response,
        '<input name="item_text" id="id_new_item" placeholder="Enter a to-do item" />',
        html=True,
    )


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


def test_saving_and_retrieving_items():
    mylist = List()
    mylist.save()

    first_item = Item()
    first_item.text = "The first (ever) list item"
    first_item.list = mylist
    first_item.save()

    second_item = Item()
    second_item.text = "Item the second"
    second_item.list = mylist
    second_item.save()

    saved_list = List.objects.get()
    assert saved_list == mylist

    saved_items = Item.objects.all()
    assert saved_items.count() == 2

    first_saved_item = saved_items[0]
    second_saved_item = saved_items[1]

    assert first_saved_item.text == "The first (ever) list item"
    assert first_saved_item.list == mylist
    assert second_saved_item.text == "Item the second"
    assert second_saved_item.list == mylist

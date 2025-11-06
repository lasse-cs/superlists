import pytest

from lists.models import Item, List


pytestmark = pytest.mark.django_db


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

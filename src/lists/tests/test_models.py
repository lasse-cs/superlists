import pytest

from django.core.exceptions import ValidationError
from django.db.utils import IntegrityError


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


def test_cannot_save_null_list_items():
    mylist = List.objects.create()
    item = Item(list=mylist, text=None)
    with pytest.raises(IntegrityError):
        item.save()


def test_cannot_save_empty_list_items():
    mylist = List.objects.create()
    item = Item(list=mylist, text="")
    with pytest.raises(ValidationError):
        item.full_clean()


def test_list_get_absolute_url():
    mylist = List.objects.create()
    assert mylist.get_absolute_url() == f"/lists/{mylist.id}/"

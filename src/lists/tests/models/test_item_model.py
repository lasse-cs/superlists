import pytest

from django.core.exceptions import ValidationError
from django.db.utils import IntegrityError


from lists.models import Item, List


pytestmark = pytest.mark.django_db


def test_default_text():
    item = Item()
    assert item.text == ""


def test_item_is_related_to_list():
    mylist = List.objects.create()
    item = Item()
    item.list = mylist
    item.save()
    assert item in mylist.item_set.all()


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


def test_duplicate_items_are_invalid():
    mylist = List.objects.create()
    Item.objects.create(list=mylist, text="bla")
    with pytest.raises(ValidationError):
        item = Item(list=mylist, text="bla")
        item.full_clean()


def test_can_save_same_item_to_different_lists():
    list1 = List.objects.create()
    list2 = List.objects.create()
    Item.objects.create(list=list1, text="bla")
    item = Item(list=list2, text="bla")
    item.full_clean()  # should not raise

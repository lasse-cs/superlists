import pytest

from lists.models import Item, List


pytestmark = pytest.mark.django_db


def test_get_absolute_url():
    mylist = List.objects.create()
    assert mylist.get_absolute_url() == f"/lists/{mylist.id}/"


def test_list_items_order():
    list1 = List.objects.create()
    item1 = Item.objects.create(list=list1, text="i1")
    item2 = Item.objects.create(list=list1, text="item 2")
    item3 = Item.objects.create(list=list1, text="3")
    assert list(list1.item_set.all()) == [item1, item2, item3]

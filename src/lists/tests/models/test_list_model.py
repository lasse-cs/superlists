import pytest

from accounts.models import User
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


def test_lists_can_have_owners():
    user = User.objects.create(email="a@b.com")
    mylist = List.objects.create(owner=user)
    assert mylist in user.lists.all()


def test_list_owner_is_optional():
    List.objects.create()  # should not raise


def test_list_name_is_first_item_text():
    list_ = List.objects.create()
    Item.objects.create(list=list_, text="first item")
    Item.objects.create(list=list_, text="second item")
    assert list_.name == "first item"


def test_lists_can_be_shared_with_a_user():
    user = User.objects.create(email="a@b.com")
    mylist = List.objects.create()
    mylist.shared_with.add(user)
    assert user in mylist.shared_with.all()

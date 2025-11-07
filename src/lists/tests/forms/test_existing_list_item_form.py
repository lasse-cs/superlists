import pytest

from lists.forms import DUPLICATE_ITEM_ERROR, EMPTY_ITEM_ERROR, ExistingListItemForm
from lists.models import Item, List


pytestmark = pytest.mark.django_db


def test_form_renders_item_text_input():
    list_ = List.objects.create()
    form = ExistingListItemForm(for_list=list_)
    assert 'placeholder="Enter a to-do item"' in form.as_p()


def test_form_validation_for_blank_items():
    list_ = List.objects.create()
    form = ExistingListItemForm(for_list=list_, data={"text": ""})
    assert not form.is_valid()
    assert form.errors["text"] == [EMPTY_ITEM_ERROR]


def test_form_validation_for_duplicate_items():
    list_ = List.objects.create()
    Item.objects.create(list=list_, text="no twins!")
    form = ExistingListItemForm(for_list=list_, data={"text": "no twins!"})
    assert not form.is_valid()
    assert form.errors["text"] == [DUPLICATE_ITEM_ERROR]


def test_form_save():
    mylist = List.objects.create()
    form = ExistingListItemForm(for_list=mylist, data={"text": "hi"})
    assert form.is_valid()
    new_item = form.save()
    assert new_item == Item.objects.get()

import pytest

from lists.models import Item, List
from lists.forms import EMPTY_ITEM_ERROR, ItemForm


def test_form_validation_for_blank_items():
    form = ItemForm(data={"text": ""})
    assert not form.is_valid()
    assert form.errors["text"] == [EMPTY_ITEM_ERROR]


@pytest.mark.django_db
def test_form_save_handles_saving_to_a_list():
    mylist = List.objects.create()
    form = ItemForm(data={"text": "do me"})
    assert form.is_valid()
    new_item = form.save(for_list=mylist)
    assert new_item == Item.objects.get()
    assert new_item.text == "do me"
    assert new_item.list == mylist

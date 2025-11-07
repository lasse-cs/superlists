import pytest

from lists.forms import EMPTY_ITEM_ERROR, ItemForm
from lists.models import Item, List


def test_form_renders_item_text_input():
    form = ItemForm()
    rendered = form.as_p()

    assert 'placeholder="Enter a to-do item"' in rendered
    assert 'class="form-control form-control-lg"' in rendered


def test_form_validation_for_blank_items():
    form = ItemForm(data={"text": ""})
    assert not form.is_valid()
    assert form.errors["text"] == [EMPTY_ITEM_ERROR]


def test_invalid_form_has_bootstrap_is_invalid_css_class():
    form = ItemForm(data={"text": ""})
    assert not form.is_valid()
    field = form.fields["text"]
    assert field.widget.attrs["class"] == "form-control form-control-lg is-invalid"


@pytest.mark.django_db
def test_form_save_handles_saving_to_a_list():
    mylist = List.objects.create()
    form = ItemForm(data={"text": "do me"})
    new_item = form.save(for_list=mylist)
    assert new_item == Item.objects.get()
    assert new_item.text == "do me"
    assert new_item.list == mylist

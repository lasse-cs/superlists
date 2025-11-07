import pytest

from lists.forms import EMPTY_ITEM_ERROR, ItemForm


def test_form_renders_item_text_input():
    form = ItemForm()
    rendered = form.as_p()

    assert 'placeholder="Enter a to-do item"' in rendered
    assert 'class="form-control form-control-lg"' in rendered


def test_form_validation_for_blank_items():
    form = ItemForm(data={"text": ""})
    assert not form.is_valid()
    assert form.errors["text"] == [EMPTY_ITEM_ERROR]

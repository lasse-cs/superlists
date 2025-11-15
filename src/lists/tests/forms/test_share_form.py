from lists.forms import EMPTY_EMAIL_ERROR, ShareForm


def test_form_validation_for_blank_email():
    form = ShareForm(data={"sharee": ""})
    assert not form.is_valid()
    assert form.errors["sharee"] == [EMPTY_EMAIL_ERROR]

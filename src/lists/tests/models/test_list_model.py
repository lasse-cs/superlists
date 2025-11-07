import pytest

from lists.models import List


pytestmark = pytest.mark.django_db


def test_get_absolute_url():
    mylist = List.objects.create()
    assert mylist.get_absolute_url() == f"/lists/{mylist.id}/"

import pytest

from pytest_django.asserts import assertContains, assertRedirects

from django.contrib.auth import get_user_model
from django.utils import html

from lists.forms import EMPTY_EMAIL_ERROR
from lists.models import List


pytestmark = pytest.mark.django_db


User = get_user_model()


def test_adds_user_to_shared_with_after_POST(client):
    list_ = List.objects.create()
    user = User.objects.create(email="edith@example.com")
    client.post(f"/lists/{list_.id}/share", data={"sharee": "edith@example.com"})
    assert user in list_.shared_with.all()


def test_redirects_to_list_page_after_POST(client):
    list_ = List.objects.create()
    user = User.objects.create(email="edith@example.com")
    response = client.post(
        f"/lists/{list_.id}/share", data={"sharee": "edith@example.com"}
    )
    assertRedirects(response, f"/lists/{list_.id}/")


def test_empty_error_ends_up_on_list_page(client):
    list_ = List.objects.create()
    response = client.post(f"/lists/{list_.id}/share", data={})
    assert response.status_code == 200
    assertContains(response, html.escape(EMPTY_EMAIL_ERROR))

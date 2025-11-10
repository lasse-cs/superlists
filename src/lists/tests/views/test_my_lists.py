import pytest

from pytest_django.asserts import assertTemplateUsed

from accounts.models import User


pytestmark = pytest.mark.django_db


def test_my_lists_url_renders_my_lists_template(client):
    User.objects.create(email="a@b.com")
    response = client.get("/lists/users/a@b.com")
    assertTemplateUsed(response, "my_lists.html")


def test_passes_correct_owner_to_template(client):
    User.objects.create(email="wrong@owner.com")
    correct_user = User.objects.create(email="a@b.com")
    response = client.get("/lists/users/a@b.com")
    assert response.context["owner"] == correct_user

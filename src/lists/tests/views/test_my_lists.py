from pytest_django.asserts import assertTemplateUsed


def test_my_lists_url_renders_my_lists_template(client):
    response = client.get("/lists/users/a@b.com")
    assertTemplateUsed(response, "my_lists.html")

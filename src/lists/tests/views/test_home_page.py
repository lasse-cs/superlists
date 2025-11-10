import lxml.html


from pytest_django.asserts import assertTemplateUsed


def test_uses_home_template(client):
    response = client.get("/")
    assertTemplateUsed(response, "home.html")


def test_renders_input_form(client):
    response = client.get("/")
    parsed = lxml.html.fromstring(response.content)
    forms = parsed.cssselect("form[method=POST]")
    assert "/lists/new" in [form.get("action") for form in forms]
    [form] = [form for form in forms if form.get("action") == "/lists/new"]
    inputs = form.cssselect("input")
    assert "text" in [input.get("name") for input in inputs]

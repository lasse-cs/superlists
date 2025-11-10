from playwright.sync_api import expect, Page


from .utils import add_list_item


def test_logged_in_users_lists_are_saved_as_my_lists(
    live_server_url: str, page: Page, pre_authenticated_session, test_email: str
):
    # Edith is a logged-in user
    pre_authenticated_session(test_email, page)

    # She goes to the home page and starts a list
    page.goto(live_server_url)

    add_list_item(page, "Reticulate splines")
    add_list_item(page, "Immanentize eschaton")
    first_list_url = page.url

    # She notices a "My lists" link, for the first time.
    my_list_link = page.get_by_role("link", name="My lists")
    my_list_link.click()

    # She sees her email is there in the page heading
    expect(page.get_by_role("heading", level=1)).to_contain_text(test_email)

    # And she sees that her list is in there,
    # named according to its first list item
    first_list_link = page.get_by_role("link", name="Reticulate splines")
    expect(first_list_link).to_be_visible()

    first_list_link.click()
    expect(page).to_have_url(first_list_url)

    # She decides to start another list, just to see
    page.goto(live_server_url)
    add_list_item(page, "Click cows")
    second_list_url = page.url

    # Under "my lists", her new list appears
    my_list_link.click()
    second_list_link = page.get_by_role("link", name="Click cows")
    second_list_link.click()
    expect(page).to_have_url(second_list_url)

    # She logs out. The "My lists" option disappears
    logout = page.get_by_role("button", "Log out")
    logout.click()
    expect(my_list_link).to_have_count(0)

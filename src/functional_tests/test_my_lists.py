from playwright.sync_api import Page


from .utils import check_logged_in, check_logged_out


def test_logged_in_users_lists_are_saved_as_my_lists(
    live_server_url: str, page: Page, pre_authenticated_session, test_email: str
):
    page.goto(live_server_url)
    check_logged_out(page, test_email)

    # Edith is a logged-in user
    pre_authenticated_session(test_email, page)
    page.goto(live_server_url)
    check_logged_in(page, test_email)

from playwright.sync_api import expect

from .list_page import ListPage
from .my_lists_page import MyListsPage


def test_can_share_a_list_with_another_user(
    live_server_url, new_context, pre_authenticated_session
):
    with new_context() as edith_ctx, new_context() as oni_ctx:
        # Edith is a logged in user
        edith_page = edith_ctx.new_page()
        pre_authenticated_session("edith@example.com", edith_page)

        # Her friend Onesiphorus is also hanging out on the lists site
        oni_page = oni_ctx.new_page()
        pre_authenticated_session("onesiphorous@example.com", oni_page)

        # Edith goes to the home page and starts a list
        edith_page.goto(live_server_url)
        edith_list_page = ListPage(edith_page).add_list_item("Get help")

        # She notices a "Share this list" option"
        share_box = edith_list_page.get_share_box()
        expect(share_box).to_have_attribute("name", "sharee")

        # She shares her list.
        # The page updates to say that it's shared with Onesiphorous
        edith_list_page.share_list_with("onesiphorous@example.com")

        # Onesiphorous now goes to the lists page with his browser
        MyListsPage(oni_page, live_server_url).go_to_my_lists_page(
            "onesiphorous@example.com"
        )

        # He sees Edith's list in there!
        oni_page.get_by_role("link", name="Get help").click()

        # On the list page, Onesiphorous can see says that it's Edith's list
        oni_list_page = ListPage(oni_page)
        expect(oni_list_page.get_list_owner()).to_have_text("edith@example.com")

        # He adds an item to the list
        oni_list_page.add_list_item("Hi Edith!")

        # When Edith refreshes the page, she sees Onesiphorous's addition
        edith_page.reload()
        edith_list_page.check_for_row_in_list_table("Hi Edith!", 2)

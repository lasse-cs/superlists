from playwright.sync_api import expect

from .utils import add_list_item


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
        add_list_item(edith_page, "Get help")

        # She notices a "Share this list" option"
        share_box = edith_page.get_by_placeholder("your-friend@example.com")
        expect(share_box).to_have_attribute("name", "sharee")

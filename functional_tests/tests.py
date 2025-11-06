import re
from playwright.sync_api import Page, expect
import pytest
import os


def check_for_row_in_list_table(page: Page, row_text: str) -> None:
    table = page.get_by_role("table")
    rows = table.get_by_role("row")
    expect(rows.filter(has_text=row_text)).to_have_count(1)

@pytest.fixture
def live_server_url(live_server):
    if test_server := os.environ.get("TEST_SERVER"):
        return "http://" + test_server
    return live_server.url


def test_can_start_a_todo_list(live_server_url: str, page: Page) -> None:
    # Edith has heard about a cool new online to-do app.
    # She goes to check out its homepage
    page.goto(live_server_url)

    # She notices the page title and header mention to-do lists
    expect(page).to_have_title(re.compile("To-Do"))
    header = page.get_by_role("heading")
    expect(header).to_have_text(re.compile("To-Do"))

    # She is invited to enter a to-do item straight away
    inputbox = page.get_by_placeholder("Enter a to-do item")
    expect(inputbox).to_be_visible()

    # She types "Buy peacock feathers" into a text box
    # (Edith's hobby is tying fly-fishing lures)
    inputbox.fill("Buy peacock feathers")

    # When she hits enter, the page updates, and now the page lists
    # "1: Buy peacock feathers" as an item in a to-do list
    inputbox.press("Enter")
    check_for_row_in_list_table(page, "1: Buy peacock feathers")

    # There is still a text box inviting her to add another item
    # She enters "Use peacock feathers to make a fly" (Edith is very methodical)
    inputbox.fill("Use peacock feathers to make a fly")
    inputbox.press("Enter")

    # The page updates again, and now shows both items on her list
    check_for_row_in_list_table(page, "2: Use peacock feathers to make a fly")
    check_for_row_in_list_table(page, "1: Buy peacock feathers")

    # Satisfied, she goes back to sleep.


def test_multiple_users_can_start_lists_at_different_urls(live_server_url: str, page: Page) -> None:
    # Edith start a new to-do list
    page.goto(live_server_url)
    inputbox = page.get_by_placeholder("Enter a to-do item")
    inputbox.fill("Buy peacock feathers")
    inputbox.press("Enter")

    check_for_row_in_list_table(page, "1: Buy peacock feathers")

    # She notices that her list has a unique URL
    expect(page).to_have_url(re.compile("/lists/.+"))
    edith_url = page.url

    # Now a new user, Francis, comes along to the site.

    ## We delete all the browser's cookies
    ## as a way of simulating a brand new user session
    page.context.clear_cookies()

    # Francis visits the home page. There is no sign of Edith's list
    page.goto(live_server_url)

    body = page.locator("body")
    expect(body).not_to_have_text(re.compile("Buy peacock feathers"))

    # Francis starts a new list by entering a new item.
    # He is less interesting than Edith...
    inputbox.fill("Buy milk")
    inputbox.press("Enter")
    check_for_row_in_list_table(page, "1: Buy milk")

    # Francis gets his own unique URL
    expect(page).to_have_url(re.compile("/lists/.+"))
    francis_url = page.url
    assert francis_url != edith_url

    # Again there is no trace of Edith's list
    expect(body).not_to_have_text(re.compile("Buy peacock feathers"))
    expect(body).to_have_text(re.compile("Buy milk"))    


def test_layout_and_styling(live_server_url: str, page: Page) -> None:
    # Edith goes to the home page, her browser window is set to a very
    # specific size
    page.set_viewport_size({"width": 1024, "height": 768})
    page.goto(live_server_url)

    # She notices the inpupt box is nicely centered
    inputbox = page.get_by_placeholder("Enter a to-do item")
    box = inputbox.bounding_box()
    assert 512 == pytest.approx(box["x"] + box["width"] / 2, abs=10)

    # She starts a new list and sees the input is nicely
    # centered there too
    inputbox.fill("testing")
    inputbox.press("Enter")

    check_for_row_in_list_table(page, "1: testing")
    box = inputbox.bounding_box()
    assert 512 == pytest.approx(box["x"] + box["width"] / 2, abs=10)

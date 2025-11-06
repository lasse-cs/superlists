from playwright.sync_api import expect, Page
import pytest

from .utils import check_for_row_in_list_table


def test_cannot_add_empty_list_items(live_server_url: str, page: Page) -> None:
    # Edith goes to the home page and accidentally tries to submit
    # an empty list item. She hits Enter on the empty input box
    page.goto(live_server_url)
    inputbox = page.get_by_placeholder("Enter a to-do item")
    inputbox.press("Enter")

    # The home page refreshes, and there is an error message saying
    # that list items cannot be blank
    invalid_label = page.get_by_text("You can't have an empty list item")
    expect(invalid_label).to_contain_class("invalid-feedback")
    
    # She tries again with some text for the item, which now works
    inputbox.fill("Purchase milk")
    inputbox.press("Enter")
    check_for_row_in_list_table(page, "1: Purchase milk")

    # Perversely, she now decides to submit a second blank list item
    inputbox.press("Enter")

    # She receives a similar warning on the list page
    invalid_label = page.get_by_text("You can't have an empty list item")
    expect(invalid_label).to_contain_class("invalid-feedback")

    # And she can correct it by filling some text in
    inputbox.fill("Make tea")
    inputbox.press("Enter")

    check_for_row_in_list_table(page, "2: Make tea")

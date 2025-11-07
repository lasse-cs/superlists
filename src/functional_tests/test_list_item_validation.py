from playwright.sync_api import expect, Page
import pytest

from .utils import check_for_row_in_list_table, get_item_input_box


def test_cannot_add_empty_list_items(live_server_url: str, page: Page) -> None:
    # Edith goes to the home page and accidentally tries to submit
    # an empty list item. She hits Enter on the empty input box
    page.goto(live_server_url)
    inputbox = get_item_input_box(page)
    inputbox.press("Enter")

    # The home page refreshes, and there is an error message saying
    # that list items cannot be blank
    invalid_input = page.locator("#id_text:invalid")
    expect(invalid_input).to_be_visible()
    
    # She starts typing some text for the new item and the error disappears
    inputbox.fill("Purchase milk")
    valid_input = page.locator("#id_text:valid")
    expect(valid_input).to_be_visible()

    # And she can submit is successfully
    inputbox.press("Enter")
    check_for_row_in_list_table(page, "1: Purchase milk")

    # Perversely, she now decides to submit a second blank list item
    inputbox.press("Enter")

    # She receives a similar warning on the list page
    expect(invalid_input).to_be_visible()

    # And she can make it happy by filling some text in
    inputbox.fill("Make tea")
    expect(valid_input).to_be_visible()
    inputbox.press("Enter")

    check_for_row_in_list_table(page, "2: Make tea")


def test_cannot_add_duplicate_items(live_server_url: str, page: Page):
    # Edith goes to the home page and starts a new list
    page.goto(live_server_url)
    inputbox = get_item_input_box(page)
    inputbox.fill("Buy wellies")
    inputbox.press("Enter")
    check_for_row_in_list_table(page, "1: Buy wellies")

    # She accidentally tries to enter a duplicate item
    inputbox.fill("Buy wellies")
    inputbox.press("Enter")

    # She gets a helpful error message
    error = page.locator(".invalid-feedback")
    expect(error).to_have_text("You've already got this in your list")

import re
from playwright.sync_api import Page, expect
import pytest


def check_for_row_in_list_table(page: Page, row_text: str) -> None:
    table = page.get_by_role("table")
    rows = table.get_by_role("row")
    expect(rows.filter(has_text=row_text)).to_have_count(1)


def test_can_start_a_todo_list(page: Page) -> None:
    # Edith has heard about a cool new online to-do app.
    # She goes to check out its homepage
    page.goto("http://localhost:8000")

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

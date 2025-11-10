import re

from playwright.sync_api import Page, expect


def check_for_row_in_list_table(page: Page, row_text: str) -> None:
    table = page.get_by_role("table")
    rows = table.get_by_role("row")
    expect(rows.filter(has_text=row_text)).to_have_count(1)


def get_item_input_box(page: Page):
    return page.get_by_placeholder("Enter a to-do item")


def check_logged_in(page: Page, email: str):
    logout_button = page.get_by_role("button", name="Log out")
    navbar = page.get_by_role("navigation")
    expect(logout_button).to_be_visible()
    expect(navbar).to_have_text(re.compile(email))


def check_logged_out(page: Page, email: str):
    loginbox = page.locator("input[name=email]")
    navbar = page.get_by_role("navigation")
    expect(loginbox).to_be_visible()
    expect(navbar).not_to_have_text(re.compile(email))


def add_list_item(page: Page, item_text: str):
    num_rows = page.get_by_role("table").get_by_role("row").count()
    inputbox = get_item_input_box(page)
    inputbox.fill(item_text)
    inputbox.press("Enter")
    check_for_row_in_list_table(page, f"{num_rows + 1}: {item_text}")

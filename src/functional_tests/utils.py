from playwright.sync_api import Page, expect


def check_for_row_in_list_table(page: Page, row_text: str) -> None:
    table = page.get_by_role("table")
    rows = table.get_by_role("row")
    expect(rows.filter(has_text=row_text)).to_have_count(1)

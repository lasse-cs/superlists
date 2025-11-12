from playwright.sync_api import expect, Page


class ListPage:
    def __init__(self, page: Page):
        self.page = page

    def get_table_rows(self):
        return self.page.get_by_role("table").get_by_role("row")

    def check_for_row_in_list_table(self, item_text, item_number):
        expected_row_text = f"{item_number}: {item_text}"
        rows = self.get_table_rows()
        expect(rows.filter(has_text=expected_row_text)).to_have_count(1)

    def get_item_input_box(self):
        return self.page.get_by_placeholder("Enter a to-do item")

    def add_list_item(self, item_text: str):
        num_rows = self.get_table_rows().count()
        inputbox = self.get_item_input_box()
        inputbox.fill(item_text)
        inputbox.press("Enter")
        self.check_for_row_in_list_table(item_text, num_rows + 1)
        return self

    def get_share_box(self):
        return self.page.get_by_placeholder("your-friend@example.com")

    def get_shared_with_list(self):
        return self.page.locator(".list-sharee")

    def share_list_with(self, email):
        share_box = self.get_share_box()
        share_box.fill(email)
        share_box.press("Enter")
        shared_with_list = self.get_shared_with_list()
        expect(shared_with_list.filter(has_text=email)).to_have_count(1)

    def get_list_owner(self):
        return self.page.locator("#id_list_owner")

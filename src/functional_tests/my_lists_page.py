from playwright.sync_api import expect, Page


class MyListsPage:
    def __init__(self, page: Page, url: str):
        self.page = page
        self.url = url

    def go_to_my_lists_page(self, email):
        self.page.goto(self.url)
        self.page.get_by_role("link", name="My lists").click()
        heading = self.page.get_by_role("heading", level="1")
        expect(heading).to_contain_text(email)
        return self

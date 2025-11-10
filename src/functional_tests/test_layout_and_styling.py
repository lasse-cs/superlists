from playwright.sync_api import Page
import pytest

from .utils import add_list_item, get_item_input_box


def test_layout_and_styling(live_server_url: str, page: Page) -> None:
    # Edith goes to the home page, her browser window is set to a very
    # specific size
    page.set_viewport_size({"width": 1024, "height": 768})
    page.goto(live_server_url)

    # She notices the inpupt box is nicely centered
    inputbox = get_item_input_box(page)
    box = inputbox.bounding_box()
    assert 512 == pytest.approx(box["x"] + box["width"] / 2, abs=10)

    # She starts a new list and sees the input is nicely
    # centered there too
    add_list_item(page, "testing")

    box = inputbox.bounding_box()
    assert 512 == pytest.approx(box["x"] + box["width"] / 2, abs=10)

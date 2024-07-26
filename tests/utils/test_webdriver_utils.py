import pytest
from selenium.webdriver.chrome.webdriver import WebDriver

from ipopy.utils.webdriver_utils import open_webdriver, setup_chrome_driver


def test_setup_chrome_driver():
    """
    Test case for the setup_chrome_driver function.

    This test verifies that the chrome driver is setup correctly and
    returns a non-None driver object.
    """
    driver = setup_chrome_driver()
    assert driver is not None
    assert isinstance(driver, WebDriver)
    assert (
        "chrome" in driver.capabilities["browserName"].lower()
    ), "Browser is not Chrome within context manager."

    driver.quit()


def test_open_webdriver():
    """
    Test the context manager for opening and closing the WebDriver.
    """
    with open_webdriver() as driver:
        assert driver is not None, "WebDriver instance is None within context manager."
        assert isinstance(driver, WebDriver)
        assert (
            "chrome" in driver.capabilities["browserName"].lower()
        ), "Browser is not Chrome within context manager."

    # After the context manager block, the WebDriver should be closed.
    with pytest.raises(Exception):
        driver.get("https://www.google.com")

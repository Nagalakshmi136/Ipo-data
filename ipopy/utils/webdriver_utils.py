from contextlib import contextmanager
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver
from ipopy.config.config_loader import CHROME_PROFILE_PATH

def setup_chrome_driver() -> webdriver.Chrome:
    """
    Initializes and returns a Chrome WebDriver instance with custom options to browse chrome.

    Returns:
    -------
    ``webdriver.Chrome``
        A configured Chrome WebDriver instance.
    """
    try:
        options = webdriver.ChromeOptions()
        options.add_experimental_option("detach", True)
        options.add_argument(CHROME_PROFILE_PATH)
        options.add_argument("--headless")  # Run in headless mode for testing
        options.add_argument("--disable-gpu")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        driver = webdriver.Chrome(
            service=Service(ChromeDriverManager().install()), options=options
        )
        return driver
    except Exception as e:
        print(f"Error occurred while setting up Chrome WebDriver: {e}")
        raise   


@contextmanager
def open_webdriver():
    """
    Context manager that opens a Chrome WebDriver instance and yields it.

    Yields:
    -------
    ``webdriver.Chrome``
        The opened Chrome WebDriver instance.
    """
    driver = setup_chrome_driver()
    try:
        yield driver
    finally:
        driver.close()
        driver.quit()
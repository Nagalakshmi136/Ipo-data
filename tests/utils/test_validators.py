from unittest.mock import MagicMock
import pytest
from ipopy.utils.validators import find_element_by_xpath, find_elements_by_xpath
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.remote.webelement import WebElement
from selenium.common.exceptions import TimeoutException


@pytest.fixture
def wait():
    """
    Fixture function that returns a mock WebDriverWait object.

    Returns:
        ``MagicMock``
            A mock WebDriverWait object.
    """
    # Create a mock WebDriverWait object
    return MagicMock(spec=WebDriverWait)


def test_find_element_by_xpath_valid(wait: MagicMock):
    """
    Test case for the function `find_element_by_xpath` when the element is found.

    Parameters:
        wait: ``MagicMock``
            A MagicMock object representing the wait object.
    """
    # Define the xpath
    xpath = "//div[@id='my-element']"

    # Mock the elements that should be returned
    mock_element = MagicMock(spec=WebElement)
    wait.until.return_value = mock_element

    # Call the function to test
    element = find_element_by_xpath(wait, xpath)

    # Assert the return value is a list containing the mock element
    assert isinstance(element, WebElement)
    assert element == mock_element


def test_find_element_by_xpath_invalid(wait: MagicMock):
    """
    Test case for the function `find_element_by_xpath` when the element is not found.

    Parameters:
        wait: ``MagicMock``
            A MagicMock object representing the wait object.

    Raises:
        ``TimeoutException``
            If the element is not found within the specified waiting time.
    """
    # Define the xpath
    xpath = "//div[@id='my-element']"

    # Simulate a timeout exception
    wait.until.side_effect = TimeoutException(
        f"Timeout occurred while waiting for element with xpath '{xpath}'"
        "Please verify the xpath or network or increase waiting time."
    )

    # Call the function and expect a TimeoutException
    with pytest.raises(TimeoutException):
        find_element_by_xpath(wait, xpath)


def test_find_elements_by_xpath_valid(wait: MagicMock):
    """
    Test case for the function `find_elements_by_xpath` when the elements are found.

    Parameters:
        wait: ``MagicMock``
            A MagicMock object representing the wait object.
    """
    # Define the xpath
    xpath = "//div[@class='my-class']"

    # Mock the elements that should be returned
    mock_elements = [MagicMock(spec=WebElement), MagicMock(spec=WebElement)]
    wait.until.return_value = mock_elements

    # Call the function to test
    elements = find_elements_by_xpath(wait, xpath)

    # Assert the return value is a list containing the mock elements
    assert isinstance(elements, list)
    assert all(isinstance(element, WebElement) for element in elements)


def test_find_elements_by_xpath_invalid(wait: MagicMock):
    """
    Test case for the function `find_elements_by_xpath` when the elements are not found.

    Parameters:
        wait: ``MagicMock``
            A MagicMock object representing the wait object.

    Raises:
        ``TimeoutException``
            If the elements are not found within the specified waiting time.
    """
    # Define the xpath
    xpath = "//div[@class='my-class']"

    # Simulate a timeout exception
    wait.until.side_effect = TimeoutException(
        f"Timeout occurred while waiting for elements with xpath '{xpath}'"
        "Please verify the xpath or network or increase waiting time."
    )

    # Call the function and expect a TimeoutException
    with pytest.raises(TimeoutException):
        find_elements_by_xpath(wait, xpath)

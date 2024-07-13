from typing import List, Literal
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.remote.webelement import WebElement
import re

def find_element_by_xpath(wait: WebDriverWait, xpath: Literal["xpath"]) -> WebElement:
    """
    Find web element using the specified XPath expression.

    Parameters:
    ----------
        wait: ``WebDriverWait``
            The WebDriverWait object used to wait for the elements to be located.
        xpath: ``Literal["xpath"]``
            The XPath expression used to locate the elements.

    Returns:
    -------
        ``List[WebElement]``
            A list of web elements that match the specified XPath expression.

    Raises:
    -------
        ``TimeoutException``
            If the elements cannot be located within the specified timeout period.
    """
    try:
        element = wait.until(EC.presence_of_element_located((By.XPATH, xpath)))
        return element
    except TimeoutException as exc_info:
        raise TimeoutException(
            f"Timeout occurred while waiting for element with xpath '{xpath}': {exc_info}."
            " Please verify the xpath or network or increase waiting time."
        ) from exc_info


def find_elements_by_xpath(
    wait: WebDriverWait, xpath: Literal["xpath"]
) -> List[WebElement]:
    """
    Find web elements using the specified XPath expression.

    Parameters:
    ----------
        wait: ``WebDriverWait``
            The WebDriverWait object used to wait for the elements to be located.
        xpath: ``Literal["xpath"]``
            The XPath expression used to locate the elements.

    Returns:
    -------
        ``List[WebElement]``
            A list of web elements that match the specified XPath expression.

    Raises:
    -------
        ``TimeoutException``
            If the elements cannot be located within the specified timeout period.
    """
    try:
        elements = wait.until(EC.presence_of_all_elements_located((By.XPATH, xpath)))
        return elements
    except TimeoutException as exc_info:
        raise TimeoutException(
            f"Timeout occurred while waiting for elements with xpath '{xpath}'"
            "Please verify the xpath or network or increase waiting time."
        ) from exc_info


def convert_to_number(currency_string: str) -> float:
    """
    Converts a currency string to a numeric value.

    Parameters:
    ----------
        currency_string: ``str``
            The currency string to be converted.

    Returns:
    -------
        ``float``
            The numeric value of the currency string.

    Raises:
    -------
        ``ValueError``
            If the string cannot be converted to a float.

    """
    cleaned_string = re.sub(r"[^\d.]", "", currency_string)
    try:
        numeric_value = float(cleaned_string)
    except ValueError as e:
        raise ValueError(
            f"Unable to convert the string to a float: {currency_string}."
        ) from e
    return numeric_value

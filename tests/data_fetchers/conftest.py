from datetime import datetime, timedelta
from typing import Any, Dict, List, Tuple
from unittest.mock import MagicMock

import pytest

from ipopy.config.config_loader import GMP_TODAY_DATE_FORMAT


def create_mock_objects_list_with_attributes(attributes: Tuple[str]) -> list[MagicMock]:
    """
    Create a list of MagicMock objects with the specified attributes.

    Parameters:
        attributes: ``Tuple[str]``
            List of attributes to be set on the MagicMock objects.

    Returns:
        ``list[MagicMock]``
            List of MagicMock objects with the specified attributes.
    """
    return [MagicMock(text=attribute) for attribute in attributes]


@pytest.fixture
def valid_mock_find_elements_by_xpath_output()-> List[MagicMock]:
    """
    Returns a valid mock output for the 'find_elements_by_xpath' method.

    This fixture creates a list of mock objects with attributes representing IPO data.
    The attributes include:
    - Name of the IPO
    - Grey market premium
    - Issue price
    - Listing price
    - Status (open or closed)
    - Start date
    - End date
    - Listing date
    - Gmp updated date

    Returns:
        ``List[MagicMock]``
            A list of mock objects representing IPO data.
    """
    return create_mock_objects_list_with_attributes(
        (
            "Ipo",
            "100",
            "500",
            "600 (20%)",
            "open",
            datetime.today().strftime(GMP_TODAY_DATE_FORMAT),
            (datetime.today() + timedelta(days=2)).strftime(GMP_TODAY_DATE_FORMAT),
            (datetime.today() + timedelta(days=2)).strftime(GMP_TODAY_DATE_FORMAT),
            (datetime.today() + timedelta(days=2)).strftime(GMP_TODAY_DATE_FORMAT),
        )
    )


@pytest.fixture
def invalid_mock_find_elements_by_xpath_output()-> List[Dict[str, Any]]:
    """
    Returns a list of dictionaries containing mock output and error messages.

    Each dictionary in the list represents a specific scenario where the output is invalid.
    The dictionary contains two keys:
    - 'output': A mock objects list with attributes representing the invalid output.
    - 'error': An error message explaining the reason for the invalid output.

    Returns:
        ``List[Dict[str, Any]]``
            A list of dictionaries representing invalid output scenarios.
    """
    return [
        {
            "output": create_mock_objects_list_with_attributes(
                (
                    "Ipo",
                    "100",
                    "600 (20%)",
                    datetime.today().strftime(GMP_TODAY_DATE_FORMAT),
                    "open",
                    (datetime.today() + timedelta(days=2)).strftime(
                        GMP_TODAY_DATE_FORMAT
                    ),
                    "500",
                    (datetime.today() + timedelta(days=2)).strftime(
                        GMP_TODAY_DATE_FORMAT
                    ),
                    (datetime.today() + timedelta(days=2)).strftime(
                        GMP_TODAY_DATE_FORMAT
                    ),
                )
            ),
            "error": f"An error occurred while converting the close date: time data '500' does not match format '{GMP_TODAY_DATE_FORMAT}'. "
            "Please verify the date format (GMP_TODAY_DATE_FORMAT) and the input string "
            "(string in cells at GMP_TODAY_COLUMNS_ORDER).",
        },
        {
            "output": create_mock_objects_list_with_attributes(
                (
                    "Ipo",
                    "open",
                    "100",
                    "500",
                    "600 (20%)",
                    datetime.today().strftime(GMP_TODAY_DATE_FORMAT),
                    (datetime.today() + timedelta(days=2)).strftime(
                        GMP_TODAY_DATE_FORMAT
                    ),
                    (datetime.today() + timedelta(days=2)).strftime(
                        GMP_TODAY_DATE_FORMAT
                    ),
                    (datetime.today() + timedelta(days=2)).strftime(
                        GMP_TODAY_DATE_FORMAT
                    ),
                )
            ),
            "error": "Unable to convert the string to a float: open.",
        },
    ]

from datetime import datetime

import pytest

from ipopy.utils.exceptions import InvalidDateFormatException
from ipopy.utils.date_utils import validate_date_format


def test_validate_date_format_valid(valid_date_format_io: list[tuple[str, datetime]]):
    """
    Test the validate_date_format function with valid date formats.

    Parameters:
        valid_date_format_io: ``list[tuple[str, datetime]]``
            A list of tuples containing a valid date format
            string and the expected datetime object.
    """
    for valid_date in valid_date_format_io:
        assert validate_date_format(valid_date[0]) == valid_date[1]


def test_validate_date_format_invalid(invalid_date_format_io: list[tuple[str, str]]):
    """
    Test case to validate the behavior of the `validate_date_format` function
    when given invalid date formats.

    Parameters:
        invalid_date_format_io: ``list[tuple[str, str]] ``
            A list of tuples where each tuple
            contains an invalid date format as the first element and 
            the expected error message as the second element.
    """
    for invalid_date in invalid_date_format_io:
        with pytest.raises(InvalidDateFormatException) as excinfo:
            validate_date_format(invalid_date[0])
        assert invalid_date[1] in str(excinfo.value)

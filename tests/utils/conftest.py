import pytest
from datetime import date


@pytest.fixture
def valid_date_format_io() -> list[tuple[str, date]]:
    """
    Returns a list of tuples representing valid date formats and their corresponding date objects.

    Returns:
        ``list[tuple[str, date]]``
            A list of tuples where each tuple contains a valid date format and its corresponding date object.
    """
    return [
        ("12-2-2021", date(2021, 2, 12)),
        ("12/oct/2022", date(2022, 10, 12)),
        ("2-Dec-2023", date(2023, 12, 2)),
        ("10-JANUARY-2024", date(2024, 1, 10)),
    ]


@pytest.fixture
def invalid_date_format_io() -> list[tuple[str, str]]:
    """
    Returns a list of invalid date formats along with their corresponding error messages.

    Returns:
        ``list[tuple[str, str]]``
            A list of invalid date formats along with their corresponding error messages.
    """
    return [
        (
            "2021-3-2",
            "Given date format 2021-3-2 is invalid. Please provide a valid date that should be in the form 'day-month-year'.",
        ),
        (
            "2021/13/2",
            "Given date format 2021/13/2 is invalid. Please provide a valid date that should be in the form 'day-month-year'.",
        ),
        (
            "",
            "Given date format  is invalid. Please provide a valid date that should be in the form 'day-month-year'.",
        ),
        (
            "jan",
            "Given date format jan is invalid. Please provide a valid date that should be in the form 'day-month-year'.",
        ),
    ]

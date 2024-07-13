from datetime import datetime, date
from ipopy.utils.exceptions import InvalidDateFormatException

def validate_date_format(target_date: str) -> date:
    """
    Validates given string is in a valid date format or not. Date must be in the form of 'day-month-year'.

    Parameters:
    -----------
    target_date: ``str``
        date to be validated.

    Exceptions:
    -----------
    ``InvalidDateFormatException``
        If the date is in wrong format.
    Return:
    -------
    ``date``
        validated given date and returns valid date object.
    """
    date_separator = "/" if len(target_date.split("/")) > 1 else "-"
    month_format_codes = ["m", "b", "B"]
    for month_format_code in month_format_codes:
        try:
            date_format = (
                f"%d{date_separator}%{month_format_code}{date_separator}%Y"
            )
            date_obj = datetime.strptime(target_date, date_format).date()
            return date_obj

        except ValueError:
            continue
    raise InvalidDateFormatException(target_date)
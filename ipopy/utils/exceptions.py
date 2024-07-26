class InvalidDateFormatException(Exception):
    """
    InvalidDateFormatException is raised when the given date format is invalid.
    """

    def __init__(self, target_date: str):
        super().__init__(
            f"Given date format {target_date} is invalid. "
            "Please provide a valid date that should be in the form 'day-month-year'."
        ),


class ContactNotFoundException(Exception):
    """
    ContactNotFoundException is raised when the specified contact is not found in the WhatsApp contact list.
    """

    def __init__(self, contact_name: str):
        super().__init__(
            f"Contact with name '{contact_name}' not found in the WhatsApp contact list. Please provide a valid contact name."
        )


class ClassNotFoundException(Exception):
    """
    ClassNotFoundException is raised when the specified class is not found in the HTML content.
    """

    def __init__(self, class_name: str):
        super().__init__(
            f"Class with name '{class_name}' not found in the HTML content. Please provide a valid class name."
        )

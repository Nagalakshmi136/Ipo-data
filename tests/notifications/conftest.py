import pytest
from datetime import datetime, timedelta
from typing import List, Tuple
from ipopy.models.ipo_data_model import IpoDataInfo


@pytest.fixture
def sample_ipo_data() -> List[Tuple[str, IpoDataInfo]]:
    """
    Fixture that returns a list of IpoDataInfo objects.

    Returns:
        ``List[IpoDataInfo]``
            A list of IpoDataInfo objects.
    """
    return [
        (
            "Gmp Today",
            IpoDataInfo(
                ipo_name="IPO1",
                premium="₹500 (50%)",
                open_date=datetime.today().strftime("%d-%m-%Y"),
                close_date=(datetime.today() + timedelta(days=2)).strftime("%d-%m-%Y"),
                price="₹1,000",
                allotment_date=(datetime.today() + timedelta(days=3)).strftime(
                    "%d-%m-%Y"
                ),
                listing_date=(datetime.today() + timedelta(days=4)).strftime(
                    "%d-%m-%Y"
                ),
            ),
        ),
        (
            "Ipo Premium",
            IpoDataInfo(
                ipo_name="IPO2",
                premium="₹600 (60%)",
                open_date=datetime.today().strftime("%d-%m-%Y"),
                close_date=(datetime.today() + timedelta(days=3)).strftime("%d-%m-%Y"),
                price="₹1,200",
                allotment_date=(datetime.today() + timedelta(days=4)).strftime(
                    "%d-%m-%Y"
                ),
                listing_date=(datetime.today() + timedelta(days=5)).strftime(
                    "%d-%m-%Y"
                ),
            ),
        ),
    ]


@pytest.fixture
def invalid_contacts() -> List[str]:
    """
    Fixture that returns a list of invalid contact inputs.

    Returns:
        ``List[str]``
            A list of invalid contact inputs.
    """
    return [
        "",
        "Invalid Contact",
        "dhoni",
        "rdj",
    ]

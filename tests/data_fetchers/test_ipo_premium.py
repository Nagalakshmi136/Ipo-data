from datetime import date, timedelta
from unittest.mock import MagicMock, patch

import pytest
import requests

from ipopy.data_classes.ipo_data_class import IpoDataInfo
from ipopy.data_fetchers.ipo_premium import IpoPremiumFetcher
from ipopy.utils.exceptions import ClassNotFoundException


@pytest.fixture
def ipo_premium_fetcher():
    """
    Returns an instance of the IpoPremiumFetcher class.
    """
    return IpoPremiumFetcher()


def test_get_data_returns_valid_data(ipo_premium_fetcher: IpoPremiumFetcher):
    """
    Test that the `get_data` method of `IpoPremiumFetcher` returns valid data.

    It checks if the returned data is a list and
    if all the items in the list are instances of `IpoDataInfo`.

    Parameters:
        ipo_premium_fetcher: ``IpoPremiumFetcher``
            An instance of the `IpoPremiumFetcher` class.
    """
    current_date = date.today()
    data = ipo_premium_fetcher.get_data(current_date)
    assert isinstance(data, tuple)
    assert isinstance(data[0], str)
    assert all(isinstance(item, IpoDataInfo) for item in data[1])


def test_get_data_handles_connection_error(
    ipo_premium_fetcher: IpoPremiumFetcher, monkeypatch: pytest.MonkeyPatch
):
    """
    Test that the `get_data` method of `IpoPremiumFetcher` handles connection errors correctly.

    It mocks the `requests.get` function to raise a `requests.exceptions.ConnectionError` and
    checks if the method raises the same exception.

    Parameters:
        ipo_premium_fetcher: ``IpoPremiumFetcher``
            An instance of the `IpoPremiumFetcher` class.
        monkeypatch: ``pytest.MonkeyPatch``
            A pytest fixture that can be used to modify the behavior of functions or classes.
    """

    def mock_requests_get(*args, **kwargs):
        raise requests.exceptions.ConnectionError("Connection error")

    monkeypatch.setattr(requests, "get", mock_requests_get)

    current_date = date.today()
    with pytest.raises(requests.exceptions.ConnectionError):
        ipo_premium_fetcher.get_data(current_date)


def test_get_data_returns_empty_list_for_long_future_date(
    ipo_premium_fetcher: IpoPremiumFetcher,
):
    """
    Test that the `get_data` method of `IpoPremiumFetcher` returns an empty list
    for a future date that is too far in the future.

    Parameters:
        ipo_premium_fetcher: ``IpoPremiumFetcher``
            An instance of the `IpoPremiumFetcher` class.
    """
    future_date = date.today() + timedelta(days=30)
    data = ipo_premium_fetcher.get_data(future_date)
    assert len(data[1]) == 0


@patch("requests.get")
def test_get_data_for_invalid_table_class(
    mock_requests_get: MagicMock,
    ipo_premium_fetcher: IpoPremiumFetcher,
):
    """
    Test that the `get_data` method of `IpoPremiumFetcher` raises an exception
    when the table class is not found in the HTML response.
    """
    mock_requests_get.return_value.content = b"<html></html>"
    with pytest.raises(ClassNotFoundException):
        ipo_premium_fetcher.get_data(date.today())

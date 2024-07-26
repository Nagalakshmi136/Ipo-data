from datetime import date
from typing import Any, Dict, List
from unittest.mock import MagicMock, patch

import pytest
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support.ui import WebDriverWait

from ipopy.data_classes.ipo_data_class import IpoDataInfo
from ipopy.data_fetchers.gmp_today import GmpTodayDataFetcher


@pytest.fixture
def gmp_today_data_fetcher() -> GmpTodayDataFetcher:
    """
    Fixture function that returns an instance of GmpTodayDataFetcher.

    Returns:
    -------
    ``GmpTodayDataFetcher``
        An instance of GmpTodayDataFetcher.
    """
    return GmpTodayDataFetcher()


@patch("ipopy.data_fetchers.gmp_today.find_elements_by_xpath")
def test_get_data_returns_valid_data(
    mock_find_elements_by_xpath: MagicMock,
    gmp_today_data_fetcher: GmpTodayDataFetcher,
    valid_mock_find_elements_by_xpath_output: List[MagicMock],
):
    """
    Test case to verify that the `get_data` method of `GmpTodayDataFetcher` returns valid data.

    Parameters:
        mock_find_elements_by_xpath: ``MagicMock``
            The mocked find_elements_by_xpath function.
        gmp_today_data_fetcher: ``GmpTodayDataFetcher``
            An instance of the GmpTodayDataFetcher class.
        valid_mock_find_elements_by_xpath_output: ``List[MagicMock]``
            A list of MagicMock objects representing the output of the find_elements_by_xpath function.
    """
    # Mocking the find_elements_by_xpath to return valid data.
    mock_find_elements_by_xpath.side_effect = valid_mock_find_elements_by_xpath_output

    current_date = date.today()
    data = gmp_today_data_fetcher.get_data(current_date)

    assert isinstance(data, tuple)
    assert isinstance(data[0], str)
    assert all(isinstance(item, IpoDataInfo) for item in data[1])


@patch("ipopy.data_fetchers.gmp_today.find_elements_by_xpath")
def test_get_data_for_invalid_xpaths(
    mock_find_elements_by_xpath: MagicMock, gmp_today_data_fetcher: GmpTodayDataFetcher
):
    """
    Test case to verify the behavior of the get_data method when invalid xpaths are provided.

    Parameters:
        mock_find_elements_by_xpath: ``MagicMock``
            The mocked find_elements_by_xpath function.
        gmp_today_data_fetcher: ``GmpTodayDataFetcher``
            An instance of the GmpTodayDataFetcher class.

    Raises:
        ``TimeoutException``
            If a timeout occurs while waiting for an element with xpath.

    """
    current_date = date.today()

    # Mocking the find_elements_by_xpath to raise an for the first time i.e. for rows xpath of the table.
    mock_find_elements_by_xpath.side_effect = TimeoutException(
        "Timeout occurred while waiting for element with xpath"
    )
    with pytest.raises(TimeoutException):
        gmp_today_data_fetcher.get_data(current_date)

    # Mocking the find_elements_by_xpath to raise an for the second time i.e. for columns xpath of the table.
    mock_find_elements_by_xpath.side_effect = [
        [MagicMock()],
        TimeoutException("Timeout occurred while waiting for element with xpath"),
    ]
    with pytest.raises(TimeoutException):
        gmp_today_data_fetcher.get_data(current_date)


@patch("ipopy.data_fetchers.gmp_today.find_elements_by_xpath")
def test_get_data_for_changed_positions_of_elements(
    mock_find_elements_by_xpath: MagicMock,
    gmp_today_data_fetcher: GmpTodayDataFetcher,
    invalid_mock_find_elements_by_xpath_output: List[Dict[str, Any]],
):
    """
    Test case for the `get_data` method of `GmpTodayDataFetcher` class.

    This test case verifies the behavior of the `get_data` method when the positions of web elements change.
    It mocks the `find_elements_by_xpath` method and provides different outputs to simulate different scenarios.
    The test checks if the method raises a `ValueError` with the expected error message.

    Parameters:
        mock_find_elements_by_xpath: ``MagicMock``
            A MagicMock object representing the `find_elements_by_xpath` function.
        gmp_today_data_fetcher: ``GmpTodayDataFetcher``
            An instance of the `GmpTodayDataFetcher` class.
        invalid_mock_find_elements_by_xpath_output: ``List[Dict[str, Any]]``
            A list of dictionaries containing mock output and error messages.
    """
    current_date = date.today()

    # Mocking the find_elements_by_xpath to return invalid data.
    for mock_data in invalid_mock_find_elements_by_xpath_output:
        mock_find_elements_by_xpath.side_effect = [[MagicMock()], mock_data["output"]]
        with pytest.raises(ValueError) as exc_info:
            gmp_today_data_fetcher.get_data(current_date)
        assert str(exc_info.value) == mock_data["error"]

from datetime import date
from typing import List, Tuple
from unittest.mock import MagicMock, patch

import pytest
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.remote.webelement import WebElement

from ipopy.config.config_loader import WHATSAPP_SEARCH_BOX_XPATH
from ipopy.data_classes.ipo_data_class import IpoDataInfo
from ipopy.notifications.whatsapp_notifier import WhatsappNotifier
from ipopy.utils.exceptions import ContactNotFoundException
from ipopy.utils.urls import WHATSAPP_URL


@pytest.fixture
def whatsapp_notifier() -> WhatsappNotifier:
    return WhatsappNotifier(target_date=date.today().strftime("%d-%m-%Y"))


@patch("time.sleep")
@patch("selenium.webdriver.support.ui.WebDriverWait")
@patch("ipopy.utils.webdriver_utils.open_webdriver")
@patch("ipopy.utils.validators.find_element_by_xpath")
def test_send_notification(
    mock_find_element_by_xpath: MagicMock,
    mock_open_webdriver: MagicMock,
    mock_webdriverwait: MagicMock,
    mock_sleep: MagicMock,
    whatsapp_notifier: WhatsappNotifier,
    sample_ipo_data: list[tuple[str, list[IpoDataInfo]]],
    valid_contact_names: list[str],
):
    """Test case to verify that IPO data can be successfully sent to a valid WhatsApp contact.

    Parameters:
    -----------
    mock_find_element_by_xpath: MagicMock
        Mock object for ipopy.utils.validators.find_element_by_xpath.
    mock_open_webdriver: MagicMock
        Mock object for ipopy.utils.webdriver_utils.open_webdriver.
    mock_webdriverwait: MagicMock
        Mock object for selenium.webdriver.support.ui.WebDriverWait.
    mock_sleep: MagicMock
        Mock object for time.sleep.
    whatsapp_notifier: WhatsappNotifier
        An instance of WhatsappNotifier.
    sample_ipo_data: list[tuple[str, list[IpoDataInfo]]]
        A list of tuples containing IPO data information.
    valid_contact_names: list[str]
        A list of valid contact names.

    Returns:
    --------
    None
    """
    mock_driver = MagicMock()
    mock_open_webdriver.return_value.__enter__.return_value = mock_driver

    mock_wait = MagicMock()
    mock_webdriverwait.return_value = mock_wait
    whatsapp_notifier.find_contact = MagicMock()
    whatsapp_notifier.send_message = MagicMock()
    for contact_name in valid_contact_names:
        whatsapp_notifier.send_notification(contact_name, sample_ipo_data)


@patch("ipopy.notifications.whatsapp_notifier.WebDriverWait")
def test_find_contact(mock_wait: MagicMock, whatsapp_notifier: WhatsappNotifier):
    """Test case to verify that a contact can be found and selected in WhatsApp.

    Parameters:
    -----------
    mock_wait: `MagicMock`
        A mock object for WebDriverWait.
    whatsapp_notifier: `WhatsappNotifier`
        An instance of WhatsappNotifier.
    """
    mock_contact = MagicMock()
    mock_search = MagicMock()
    # Mock the methods to find elements
    with patch("ipopy.utils.validators.find_element_by_xpath") as mock_find_element:
        mock_find_element.side_effect = [mock_search, mock_contact]

        whatsapp_notifier.find_contact(mock_wait, "Test Contact")

        # Check if the contact was searched and selected
        mock_find_element.assert_any_call(mock_wait, WHATSAPP_SEARCH_BOX_XPATH)
        mock_search.send_keys.assert_called_with("Test Contact")
        mock_contact.click.assert_called_once()


def test_send_notification_with_data(
    sample_ipo_data: List[Tuple[str, List[IpoDataInfo]]],
    whatsapp_notifier: WhatsappNotifier,
):
    """Test case to verify that IPO data message can be successfully sent to a WhatsApp contact.

    Parameters:
    -----------
    sample_ipo_data: `List[Tuple[str, List[IpoDataInfo]]]`
        A list of tuples containing IPO data information.
    whatsapp_notifier: `WhatsappNotifier`
        An instance of WhatsappNotifier.
    """
    # Check if messages were sent
    mock_input_field = MagicMock(spec=WebElement)
    for source_website, ipo_data in sample_ipo_data:
        whatsapp_notifier.send_message(mock_input_field, ipo_data, source_website)
        header = f"IPO data from {source_website} website: "
        mock_input_field.send_keys.assert_any_call(header + Keys.ENTER)
        for data_entry in ipo_data:
            for line in str(data_entry).split("\n"):
                mock_input_field.send_keys.assert_any_call(
                    line + Keys.SHIFT + Keys.ENTER
                )
            mock_input_field.send_keys.assert_any_call(Keys.ENTER)


def test_send_message_with_no_data(whatsapp_notifier: WhatsappNotifier):
    """Test case for sending a message with no IPO data.

    Parameters:
    -----------
    whatsapp_notifier: `WhatsappNotifier`
        An instance of WhatsappNotifier.
    """
    # Mock the methods to find elements
    mock_input_field = MagicMock(spec=WebElement)
    empty_ipo_data_with_sources = [("IPO Premium", []), ("GMP Today", [])]
    for source_website, ipo_data in empty_ipo_data_with_sources:
        whatsapp_notifier.send_message(mock_input_field, ipo_data, source_website)
        header = f"IPO data from {source_website} website: "
        mock_input_field.send_keys.assert_any_call(header + Keys.ENTER)
        no_data_message = (
            f"No IPO data available for the date {whatsapp_notifier.target_date}."
        )
        mock_input_field.send_keys.assert_any_call(no_data_message + Keys.ENTER)


@patch("ipopy.notifications.whatsapp_notifier.open_webdriver")
@patch("ipopy.notifications.whatsapp_notifier.WebDriverWait")
def test_find_contact_not_found(
    mock_webdriverwait: MagicMock,
    mock_open_webdriver: MagicMock,
    whatsapp_notifier: WhatsappNotifier,
    sample_ipo_data: List[Tuple[str, List[IpoDataInfo]]],
):
    """Test case for when a contact is not found in WhatsApp.

    Parameters:
    -----------
    mock_webdriverwait: `MagicMock`
        A Mock object for WebDriverWait.
    mock_open_webdriver: `MagicMock`
        Mock object for ipopy.utils.webdriver_utils.open_webdriver.
    whatsapp_notifier: `WhatsappNotifier`
        An instance of WhatsappNotifier.
    sample_ipo_data: `List[Tuple[str, List[IpoDataInfo]]]`
        A list of tuples containing IPO data information.
    """
    mock_driver = MagicMock()
    mock_open_webdriver.return_value.__enter__.return_value = mock_driver

    mock_wait = MagicMock()
    mock_webdriverwait.return_value = mock_wait

    with patch("ipopy.utils.validators.find_element_by_xpath") as mock_find_element:
        mock_find_element.side_effect = [MagicMock(), Exception("Element not found")]

        with pytest.raises(ContactNotFoundException):
            whatsapp_notifier.send_notification("Non-existent Contact", sample_ipo_data)

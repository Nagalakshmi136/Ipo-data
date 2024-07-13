import pytest
from datetime import date
from unittest.mock import patch, MagicMock
from ipopy.utils.exceptions import ContactNotFoundException, InvalidDateFormatException
from ipopy.notifications.whatsapp_sender import WhatsappSender
from ipopy.models.ipo_data_model import IpoDataInfo


@pytest.fixture
def whatsapp_sender(sample_ipo_data) -> WhatsappSender:
    """
    Fixture function that returns an instance of WhatsappSender.

    Returns:
    -------
    ``WhatsappSender``
        An instance of WhatsappSender.
    """
    return WhatsappSender(
        contact_name="Test",
        target_date=date.today().strftime("%d-%m-%Y"),
        ipo_data=sample_ipo_data,
    )


@patch("time.sleep")
@patch("ipopy.utils.webdriver_utils.open_webdriver")
@patch("ipopy.utils.validators.find_element_by_xpath")
def test_send_data(
    mock_find_element_by_xpath: MagicMock,
    mock_open_webdriver: MagicMock,
    mock_sleep: MagicMock,
    whatsapp_sender: WhatsappSender,
):
    """Test case to verify that IPO data can be successfully sent to a valid WhatsApp contact.

    Parameters:
    -----------
    mock_open_webdriver: `MagicMock`
        Mock object for webdriver_utils.open_webdriver.
    mock_sleep: `MagicMock`
        Mock object for time.sleep.
    whatsapp_sender: `WhatsappSender`
        An instance of WhatsappSender.
    """
    mock_driver = MagicMock()
    mock_open_webdriver.return_value.__enter__.return_value = mock_driver
    whatsapp_sender._find_contact = MagicMock()
    whatsapp_sender._send_message = MagicMock()
    whatsapp_sender.send_data()
    whatsapp_sender._find_contact.assert_called_once_with(MagicMock(), "Test Contact")
    whatsapp_sender._send_message.assert_called()


@patch("ipopy.utils.validators.find_element_by_xpath")
@patch("ipopy.utils.webdriver_utils.open_webdriver")
def test_send_data_invalid_contact(
    mock_open_webdriver: MagicMock,
    mock_find_element_by_xpath: MagicMock,
    whatsapp_sender: WhatsappSender,
    invalid_contacts: list[str],
):
    """Test case to verify that an exception is raised when the contact is not found on WhatsApp.

    Parameters:
    -----------
    mock_open_webdriver: `MagicMock`
        Mock object for webdriver_utils.open_webdriver.
    mock_find_element_by_xpath: `MagicMock`
        Mock object for validators.find_element_by_xpath.
    whatsapp_sender: ``WhatsappSender``
        An instance of WhatsappSender.
    invalid_contacts: ``list[str]``
        List of invalid contact names.

    Raises:
    -------
    `ContactNotFoundException`
        If the contact is not found on WhatsApp.
    """
    mock_driver = MagicMock()
    mock_open_webdriver.return_value.__enter__.return_value = mock_driver
    

    with pytest.raises(ContactNotFoundException):
        whatsapp_sender._find_contact()


# @patch("ipopy.utils.validators.find_element_by_xpath")
# @patch("ipopy.utils.webdriver_utils.ChromeDriverSingleton.get_instance")
# @patch("ipopy.ipo_premium.IpoPremiumFetcher.get_data")
# @patch("ipopy.gmp_today.GmpTodayDataFetcher.get_data")
# def test_send_ipo_data_to_whatsapp_contact_not_found(
#     mock_gmp_get_data: MagicMock,
#     mock_ipo_get_data: MagicMock,
#     mock_get_instance: MagicMock,
#     mock_find_element_by_xpath: MagicMock,
#     invalid_contact_io: list[str],
#     gmp_and_ipo_outputs: list[IpoDataInfo],
# ):
#     """
#     Test case to verify that an exception is raised when the contact is not found on WhatsApp.

#     Parameters:
#         mock_gmp_get_data: ``MagicMock``
#             Mock object for GmpTodayDataFetcher.get_data.
#         mock_ipo_get_data: ``MagicMock``
#             Mock object for IpoPremiumFetcher.get_data.
#         mock_get_instance: ``MagicMock``
#             Mock object for ChromeDriverSingleton.get_instance.
#         mock_find_element_by_xpath: ``MagicMock``
#             Mock object for validators.find_element_by_xpath.
#         invalid_contact_io: ``list[str]``
#             List of invalid contact names.
#         gmp_and_ipo_outputs: ``list[IpoDataInfo]``
#             List of IpoDataInfo objects.

#     Raises:
#         ContactNotFoundException: If the contact is not found on WhatsApp.

#     """
#     driver_mock = MagicMock()
#     mock_get_instance.return_value = driver_mock
#     mock_ipo_get_data.return_value = gmp_and_ipo_outputs
#     mock_gmp_get_data.return_value = gmp_and_ipo_outputs
#     mock_search_box = MagicMock()
#     for contact_name in invalid_contact_io:
#         mock_find_element_by_xpath.side_effect = [
#             mock_search_box,
#             Exception("An error occurred while finding the xpath"),
#         ]
#         with pytest.raises(ContactNotFoundException):
#             send_ipo_data_to_whatsapp_contact(contact_name)
#         driver_mock.quit.assert_called_once()
#         driver_mock.reset_mock()


# def test_send_ipo_data_to_whatsapp_contact_invalid_date_format(
#     invalid_date_io: list[tuple[str, str]]
# ):
#     """
#     Test case to verify that an exception is raised when the date format is invalid.

#     Parameters:
#         invalid_date_io: ``list[tuple[str, str]]``
#             List of invalid contact names and target dates.

#     Raises:
#         ``InvalidDateFormatException``
#             If the date format is invalid.

#     """
#     for contact_name, target_date in invalid_date_io:
#         with pytest.raises(InvalidDateFormatException):
#             send_ipo_data_to_whatsapp_contact(contact_name, target_date)

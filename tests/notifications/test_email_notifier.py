from datetime import date
from email.mime.multipart import MIMEMultipart
from unittest.mock import MagicMock, patch

import pytest

from ipopy.notifications.email_notifier import EmailNotifier

# Constants for the test
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 465
SENDER_EMAIL = "testsender@gmail.com"
APP_PASSWORD = "app_password"
RECIPIENT_EMAIL = "recipient@gmail.com"
TARGET_DATE = date.today().strftime("%d-%m-%Y")


@pytest.fixture
def email_notifier() -> EmailNotifier:
    "Fixture to create an EmailNotifier object."
    return EmailNotifier(
        sender_email=SENDER_EMAIL, app_password=APP_PASSWORD, target_date=TARGET_DATE
    )


def test_attach_ipo_data_to_email(
    email_notifier: EmailNotifier, sample_ipo_data: list[tuple[str, list]]
):
    """Test case to verify that IPO data can be successfully attached to an email.

    Parameters:
    -----------
    email_notifier: `EmailNotifier`
        An instance of EmailNotifier.
    sample_ipo_data: `list[tuple[str, list[IpoDataInfo]]]`
        A list of tuples containing IPO data information.
    """
    for source, ipo_data in sample_ipo_data:
        email_message = MIMEMultipart()
        email_notifier.attach_ipo_data_to_email(email_message, ipo_data, source)
        assert (
            email_message.get_payload()[0].get_payload()
            == f"IPO data from {source} website: \n"
        )
        assert email_message.get_payload()[1].get_payload(decode=True).decode() == str(
            ipo_data[0]
        )


def test_attach_ipo_data_to_email_no_data(email_notifier):
    """Test case to verify when there is no IPO data available to attach to the email.

    Parameters:
    -----------
    email_notifier: `EmailNotifier`
        An instance of EmailNotifier.
    """
    email_message = MIMEMultipart()
    email_notifier.attach_ipo_data_to_email(email_message, [], "Test Source")

    assert (
        email_message.get_payload()[0].get_payload()
        == "IPO data from Test Source website: \n"
    )
    assert (
        email_message.get_payload()[1].get_payload()
        == f"No IPO data available for the date {TARGET_DATE}."
    )


@patch("smtplib.SMTP_SSL")
def test_send_notification(
    mock_smtp_ssl: MagicMock,
    email_notifier: EmailNotifier,
    sample_ipo_data: list[tuple[str, list]],
):
    """Test case for sending an email notification with IPO data.

    Parameters:
    -----------
    mock_smtp_ssl: `MagicMock`
        A Mock object for smtplib.SMTP_SSL.
    email_notifier: `EmailNotifier`
        An instance of EmailNotifier.
    sample_ipo_data: `list[tuple[str, list]]`
        A list of tuples containing IPO data information.
    """
    mock_smtp = MagicMock()
    mock_smtp_ssl.return_value.__enter__.return_value = mock_smtp

    email_notifier.send_notification(RECIPIENT_EMAIL, sample_ipo_data)
    # Verify email content
    email_message = mock_smtp.sendmail.call_args[0][2]
    assert f"IPO data from Ipo Premium website: \n" in email_message
    assert f"IPO data from Gmp Today website: \n" in email_message

    # Verify SMTP methods were called
    mock_smtp_ssl.assert_called_with(SMTP_SERVER, SMTP_PORT)
    mock_smtp.login.assert_called_with(SENDER_EMAIL, APP_PASSWORD)
    mock_smtp.sendmail.assert_called_once()


@patch("smtplib.SMTP_SSL")
def test_send_notification_no_data(
    mock_smtp_ssl: MagicMock, email_notifier: EmailNotifier
):
    """Test case for sending an email notification with no IPO data.

    Parameters:
    -----------
    mock_smtp_ssl: `MagicMock`
        A Mock object for smtplib.SMTP_SSL.
    email_notifier: `EmailNotifier`
        An instance of EmailNotifier.
    """
    mock_smtp = MagicMock()
    mock_smtp_ssl.return_value.__enter__.return_value = mock_smtp

    empty_ipo_data_with_sources = [("IPO Premium", []), ("GMP Today", [])]
    email_notifier.send_notification(RECIPIENT_EMAIL, empty_ipo_data_with_sources)

    # Verify email content
    email_message = mock_smtp.sendmail.call_args[0][2]
    assert f"No IPO data available for the date {TARGET_DATE}." in email_message

    # Verify SMTP methods were called
    mock_smtp_ssl.assert_called_with(SMTP_SERVER, SMTP_PORT)
    mock_smtp.login.assert_called_with(SENDER_EMAIL, APP_PASSWORD)
    mock_smtp.sendmail.assert_called_once()

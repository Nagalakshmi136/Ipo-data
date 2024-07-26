import time
from datetime import date
from typing import List, Tuple

from selenium.webdriver.common.keys import Keys
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.ui import WebDriverWait

from ipopy.config.config_loader import (
    WHATSAPP_MESSAGE_TEXTFIELD_XPATH,
    WHATSAPP_SEARCH_BOX_XPATH,
)
from ipopy.data_classes.ipo_data_class import IpoDataInfo
from ipopy.notifications.notifier import Notifier
from ipopy.utils import validators
from ipopy.utils.exceptions import ContactNotFoundException
from ipopy.utils.urls import WHATSAPP_URL
from ipopy.utils.webdriver_utils import open_webdriver


@Notifier.register("whatsapp")
class WhatsappNotifier(Notifier):
    """
    A class for sending IPO data via WhatsApp Web.
    """

    def __init__(
        self,
        target_date: str = date.today().strftime("%d-%m-%Y"),
    ):
        """
        Initialize the WhatsappSender object.

        Parameters:
        ----------
            target_date: ``str``
                The target date from which the IPO data is fetched to sent.
        """
        self.target_date = target_date

    def send_message(
        self,
        input_field: WebElement,
        ipo_data_list: List[IpoDataInfo],
        source_website: str,
    ) -> None:
        """
        Sends the message of IPO data in a readable format to the target contact or group.

        Parameters:
        ----------
            input_field: ``WebElement``
                The WebElement object representing the input field of the
                WhatsApp Web chat box to send messages.
            ipo_data: ``List[IpoDataInfo]``
                A list of IPO data entries.
            source_website: ``str``
                The source website of the IPO data.

        """
        header = f"IPO data from {source_website} website: "
        input_field.send_keys(header + Keys.ENTER)

        if not ipo_data_list:
            no_data_message = f"No IPO data available for the date {self.target_date}."
            input_field.send_keys(no_data_message + Keys.ENTER)
        else:
            for data_entry in ipo_data_list:
                for line in str(data_entry).split("\n"):
                    input_field.send_keys(line + Keys.SHIFT + Keys.ENTER)
                input_field.send_keys(Keys.ENTER)

    def find_contact(self, wait: WebDriverWait, contact_names: str) -> None:
        """
        Find and select the contact or group with the given name.

        Parameters:
        ----------
            wait: ``WebDriverWait``
                The WebDriverWait object.
            contact_names: ``str``
                The name of the contact or group to find.

        Raises:
        -------
            ``ContactNotFoundException``
                If the contact or group is not found.

        """
        search_box = validators.find_element_by_xpath(wait, WHATSAPP_SEARCH_BOX_XPATH)
        search_box.send_keys(contact_names)
        try:
            contact = validators.find_element_by_xpath(
                wait, f'//span[@title="{contact_names}"]'
            )
            contact.click()

        except Exception as exc_info:
            raise ContactNotFoundException(contact_names) from exc_info

    def send_notification(
        self,
        contact_name: str,
        ipo_data_with_sources: List[Tuple[str, IpoDataInfo]],
    ) -> None:
        """Sends a WhatsApp message to the given contact list or group with the IPO data.

        Parameters:
        -----------
        contact_name: `str`
            The name of the contact or group to send the message to.
        ipo_data_with_sources: `List[Tuple[str, IpoDataInfo]]`
            A list of tuples containing the source website and IPO data.
        """

        with open_webdriver(for_whatsapp=True) as driver:
            wait = WebDriverWait(driver, 60)
            # Open WhatsApp Web
            driver.get(WHATSAPP_URL)

            # Search for the given WhatsApp contact or group.
            self.find_contact(wait, contact_name)

            # Get the input field to send messages to the target group
            input_field = validators.find_element_by_xpath(
                wait, WHATSAPP_MESSAGE_TEXTFIELD_XPATH
            )

            # Send IPO data to the given contact or group
            for source_website, ipo_data_list in ipo_data_with_sources:
                self.send_message(input_field, ipo_data_list, source_website)
            # Wait for 30 seconds before quitting the driver
            time.sleep(60)
            print("Message sent successfully!")

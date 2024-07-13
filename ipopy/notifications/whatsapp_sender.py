from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
import time
from typing import Tuple, List
from ipopy.models.ipo_data_model import IpoDataInfo
from ipopy.utils.urls import WHATSAPP_URL
from ipopy.utils import validators
from ipopy.utils.webdriver_utils import open_webdriver
from ipopy.utils.exceptions import ContactNotFoundException
from selenium.webdriver.remote.webelement import WebElement
from ipopy.config.config_loader import (
    WHATSAPP_MESSAGE_TEXTFIELD_XPATH,
    WHATSAPP_SEARCH_BOX_XPATH,
)


class WhatsappSender:
    """
    A class for sending IPO data via WhatsApp Web.
    """

    def __init__(
        self,
        contact_names: List[str],
        target_date: str,
        ipo_data: List[Tuple[str, IpoDataInfo]],
    ):
        """
        Initialize the WhatsappSender object.

        Parameters:
        ----------
            contact_names: ``List[str]``
                The list of names of the contact or group to send the messages to.
            target_date: ``str``
                The target date from which the IPO data is fetched to sent.
            ipo_data: ``List[Tuple[str, IpoDataInfo]])``
                A list of tuples containing the source website and IPO data.

        """
        self.contact_names = contact_names
        self.target_date = target_date
        self.ipo_data = ipo_data

    def _send_message(
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

    def _find_contact(self, wait: WebDriverWait, contact_names: str) -> None:
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

    def send_data(self) -> None:
        """
        Send the IPO data to the specified list of contacts or groups on WhatsApp Web.

        """
        with open_webdriver() as driver:
            wait = WebDriverWait(driver, 60)
            # Open WhatsApp Web
            driver.get(WHATSAPP_URL)

            for contact_name in self.contact_names:
                # Search for the given WhatsApp contact or group.
                self._find_contact(wait, contact_name)

                # Get the input field to send messages to the target group
                input_field = validators.find_element_by_xpath(
                    wait, WHATSAPP_MESSAGE_TEXTFIELD_XPATH
                )

                # Send IPO data to the given contact or group
                for source_website, ipo_data_list in self.ipo_data:
                    self._send_message(input_field, ipo_data_list, source_website)
                # Wait for 30 seconds before quitting the driver
                time.sleep(30)
                print("Message sent successfully!")

from datetime import date
from typing import List, Optional
from ipopy.notifications.whatsapp_sender import WhatsappSender
from ipopy.data_fetchers.ipo_premium import IpoPremiumFetcher
from ipopy.data_fetchers.gmp_today import GmpTodayDataFetcher
from ipopy.utils.date_utils import validate_date_format
from ipopy.notifications.email_sender import GmailSender


class IPODataHandler:
    """
    A class responsible for fetching IPO-related data and sending it via different channels like WhatsApp or Gmail.
    """

    def __init__(self, target_date: Optional[date] = None) -> None:
        """
        Initialize the IPODataHandler object.

        Parameters:
        ----------
            target_date: ``Optional[date]``
                The date for which IPO data is to be fetched. Defaults to today's date if not provided.
        """
        self.target_date = target_date or date.today()
        self.ipo_data = None

    def _fetch_ipo_data(self) -> None:
        """
        Fetches IPO data from different sources and stores it in `ipo_data` attribute.

        """

        if isinstance(self.target_date, str):
            self.target_date = validate_date_format(self.target_date)

        # Collect IPO data from IPO Premium websites
        ipo_premium_data = IpoPremiumFetcher().get_data(self.target_date)
        # Collect IPO data from GMP Today websites
        gmp_today_data = GmpTodayDataFetcher().get_data(self.target_date)
        self.ipo_data = [
            ("IPO Premium", ipo_premium_data),
            ("GMP Today", gmp_today_data),
        ]

    def send_via_whatsapp(self, contact_names: List[str]) -> None:
        """
        Sends IPO data via WhatsApp to the specified contact.

        Parameters:
        ----------
            contact_names: ``List[str]``
                The names of the contacts to whom the data is to be sent.
        """

        if not self.ipo_data:
            self._fetch_ipo_data()
        WhatsappSender(
            contact_names,
            self.target_date,
            self.ipo_data,
        ).send_data()

    def send_via_gmail(
        self, sender_email: str, app_password: str, recipient_emails: List[str]
    ) -> None:
        """
        Sends IPO data via Gmail to the specified recipient.

        Parameters:
        ----------
            sender_email: ``str``
                The sender's gmail address.
            app_password: ``str``
                The application-specific password for SMTP authentication. It's 16 characters long.
                if you want to generate a new app password for your gmail, follow these steps:
                1. Go to your Google Account.
                2. Select Security.
                3. Enable 2-Step Verification.
                4. Go through this url https://myaccount.google.com/u/4/apppasswords and give any name for the app and click on create.
                5. Copy the generated password and use it in the app_password parameter.
            recipient_emails: ``List[str]``
                The recipient's email addresses.
        """

        if not self.ipo_data:
            self._fetch_ipo_data()
        GmailSender(
            sender_email,
            app_password,
            recipient_emails,
            self.target_date,
            self.ipo_data,
        ).send_data()

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from ipopy.utils.constants import SMTP_SERVER, SMTP_PORT
from typing import List, Tuple
from ipopy.models.ipo_data_model import IpoDataInfo


class GmailSender:
    """
    A class for sending IPO data via Gmail.
    """

    def __init__(
        self,
        sender_email: str,
        app_password: str,
        recipient_emails: List[str],
        target_date: str,
        ipo_data: List[Tuple[str, List[IpoDataInfo]]],
    ):
        """
        Initialize the EmailSender object.

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
                The recipient's email address.
            target_date: ``str``
                The target date for which the IPO data is fetched to sent.
            ipo_data: ``List[Tuple[str, List[IpoDataInfo]]]``
                A list of tuples containing the source website and IPO data.

        """
        self.sender_email = sender_email
        self.app_password = app_password
        self.recipient_emails = recipient_emails
        self.target_date = target_date
        self.ipo_data = ipo_data

    def _attach_ipo_data_to_gmail(
        self,
        email_message: MIMEMultipart,
        ipo_data_list: List[IpoDataInfo],
        source_website: str,
    ) -> None:
        """
        Attaches IPO data to the email message in a readable format for the user.

        Parameters:
        ----------
            email_message: ``MIMEMultipart``
                The email message object
            ipo_data_list: ``List[IpoDataInfo]``
                The list of IPO data entries.
            source_website: ``str``
                The source website of the IPO data.

        """
        # Create a header for the email content
        header = f"IPO data from {source_website} website: \n"
        email_message.attach(MIMEText(header, "plain"))

        # Check if IPO data is empty and attach a message if so
        if not ipo_data_list:
            no_data_message = f"No IPO data available for the date {self.target_date}."
            email_message.attach(MIMEText(no_data_message, "plain"))
        else:
            # Attach each piece of IPO data to the email
            for data_entry in ipo_data_list:
                email_message.attach(MIMEText(str(data_entry), "plain"))
                # Add a newline for readability between IPO data entries
                email_message.attach(MIMEText("\n", "plain"))

    def send_data(self) -> None:
        """
        Sends the IPO data via Gmail.
        """
        # Create the email message
        email_message = MIMEMultipart()
        email_message["From"] = self.sender_email
        email_message["Subject"] = (
            f"Currently available IPO data including its grey market premium for {self.target_date}"  # Enter your subject
        )

        # Add the ipo data to the email message
        for source_website, ipo_data_list in self.ipo_data:
            self._attach_ipo_data_to_email(email_message, ipo_data_list, source_website)

        # Send the email message
        for recipient_email in self.recipient_emails:
            email_message["To"] = recipient_email
            with smtplib.SMTP_SSL(SMTP_SERVER, SMTP_PORT) as smtp:
                smtp.login(self.sender_email, self.app_password)
                smtp.sendmail(
                    self.sender_email,
                    recipient_email,
                    email_message.as_string(),
                )
            print(f"email sent successfully to {recipient_email}")

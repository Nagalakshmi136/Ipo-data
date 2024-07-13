from ipopy.utils.data_processor import process_ipo_data
from ipopy.utils.exceptions import ClassNotFoundException
import requests
from bs4 import BeautifulSoup
from datetime import datetime, date
from ipopy.config.config_loader import (
    IPO_PREMIUM_TABLE_CLASS,
    IPO_PREMIUM_DATE_FORMAT,
    IPO_PREMIUM_COLUMNS_ORDER,
)
from ipopy.models.ipo_data_model import IpoDataInfo
from ipopy.utils.urls import IPO_PREMIUM_URL


class IpoPremiumFetcher:
    """
    A class to fetch IPO data from the Ipo Premium website.
    """

    def __init__(self):
        """
        Initializes the IpoPremiumFetcher object with the Ipo Premium website URL.

        Parameters:
        ----------
            url: ``str``
                The URL to fetch the data from.
                    e.g. "https://www.ipopremium.in
        """
        self.url = IPO_PREMIUM_URL

    def get_data(self, target_date: date) -> list[IpoDataInfo]:
        """
        Fetches IPO data from the Ipo Premium website from the given target date onwards.

        This includes current and future IPO details if the information exists.

        Parameters:
        ----------
            target_date: ``datetime``
                The date from which to start fetching IPO data.

        Returns:
        -------
            ``list[IpoDataInfo]``
                Processed IPO data as a list of IpoDataInfo objects.

        """

        response = requests.get(self.url)
        soup = BeautifulSoup(response.content, "lxml")
        table = soup.find("table", class_=IPO_PREMIUM_TABLE_CLASS)
        if not table:
            raise ClassNotFoundException(IPO_PREMIUM_TABLE_CLASS)
        rows = table.find_all("tr")
        ipos_data = []

        for row in rows:
            cells = row.find_all("td")
            if len(cells) == 0:
                continue
            try:
                close_date = datetime.strptime(
                    cells[IPO_PREMIUM_COLUMNS_ORDER[3]].get_text().strip(),
                    IPO_PREMIUM_DATE_FORMAT,
                ).date()
            except ValueError as e:
                raise ValueError(
                    f"An error occurred while converting the close date: {e}. "
                    "Please verify the date format (IPO_PREMIUM_DATE_FORMAT) and the input string "
                    "(string in cells at IPO_PREMIUM_COLUMNS_ORDER)."
                ) from e
            stock_name = cells[IPO_PREMIUM_COLUMNS_ORDER[0]].get_text().strip()

            if "MAIN" in stock_name and target_date <= close_date:
                ipos_data.append(
                    [cells[i].get_text().strip() for i in IPO_PREMIUM_COLUMNS_ORDER]
                )

        return process_ipo_data(ipos_data)

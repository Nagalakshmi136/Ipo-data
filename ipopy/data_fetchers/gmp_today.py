from datetime import datetime, date

from selenium.webdriver.support.ui import WebDriverWait
from ipopy.config.config_loader import (
    GMP_TODAY_TABLE_ROWS_XPATH,
    GMP_TODAY_DATE_FORMAT,
    GMP_TODAY_COLUMNS_ORDER,
)
from ipopy.utils.webdriver_utils import open_webdriver
from ipopy.models.ipo_data_model import IpoDataInfo
from ipopy.utils.data_processor import process_ipo_data
from ipopy.utils.validators import find_elements_by_xpath, convert_to_number
from ipopy.utils.urls import GMP_TODAY_URL


class GmpTodayDataFetcher:
    """
    A class to fetch IPO data from the GMP Today website.
    """

    def __init__(self) -> None:
        """
        Initializes the GmpTodayDataFetcher object with the GMP Today website URL.

        Parameters:
        -----------
            url: ``str``.
                The URL to fetch the data from.
                    e.g. "https://www.ipopremium.in
        """
        self.url = GMP_TODAY_URL

    def get_data(self, target_date: date) -> list[IpoDataInfo]:
        """
        Fetches IPO data from the GMP Today website from the given target date onwards.

        This includes current and future IPO details if the information exists.

        Parameters:
        ----------
            target_date: ``date``
                The date from which to start fetching IPO data.

        Returns:
        -------
            ``list[IpoDataInfo]``
                Processed IPO data as a list of IpoDataInfo objects.

        """
        with open_webdriver() as driver:
            wait = WebDriverWait(driver, 60)
            driver.get(self.url)
            ipos_data = []
            rows = len(find_elements_by_xpath(wait, GMP_TODAY_TABLE_ROWS_XPATH))
            for row in range(1, rows + 1):
                cells = find_elements_by_xpath(
                    wait, f"{GMP_TODAY_TABLE_ROWS_XPATH}[{row}]/td"
                )
                try:
                    close_date = datetime.strptime(
                        cells[GMP_TODAY_COLUMNS_ORDER[3]].text, GMP_TODAY_DATE_FORMAT
                    ).date()
                except ValueError as e:
                    raise ValueError(
                        f"An error occurred while converting the close date: {e}. "
                        "Please verify the date format (GMP_TODAY_DATE_FORMAT) and the input string "
                        "(string in cells at GMP_TODAY_COLUMNS_ORDER)."
                    ) from e
                if target_date <= close_date:
                    ipos_data.append(
                        [
                            cells[column].text if column != None else None
                            for column in GMP_TODAY_COLUMNS_ORDER
                        ]
                    )
                    premium = (
                        100
                        * convert_to_number(ipos_data[-1][1])
                        / convert_to_number(ipos_data[-1][4])
                    )
                    ipos_data[-1][1] += f" ({premium:.2f}%)"
            return process_ipo_data(ipos_data)

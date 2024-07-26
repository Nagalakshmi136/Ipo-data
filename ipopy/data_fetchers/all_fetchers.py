from datetime import date
from typing import Union

from ipopy.data_classes.ipo_data_class import IpoDataInfo
from ipopy.data_fetchers.gmp_today import GmpTodayDataFetcher
from ipopy.data_fetchers.ipo_premium import IpoPremiumFetcher
from ipopy.utils.date_utils import validate_date_format


def fetch_ipo_data(
    target_date: Union[str, date] = None
) -> list[tuple[str, list[IpoDataInfo]]]:
    """
    Fetch IPO data from different sources that exist from a given date.

    Return:
    -------
    list[tuple[str, list[IpoDataInfo]]]
        A list of tuples where each tuple contains the source name and a list of IPO data.
    """
    if target_date is None or target_date == "":
        target_date = date.today()
    elif isinstance(target_date, str):
        target_date = validate_date_format(target_date)

    # Collect IPO data from IPO Premium websites
    ipo_premium_data = IpoPremiumFetcher().get_data(target_date)

    # Collect IPO data from GMP Today websites
    gmp_today_data = GmpTodayDataFetcher().get_data(target_date)
    return [ipo_premium_data, gmp_today_data]

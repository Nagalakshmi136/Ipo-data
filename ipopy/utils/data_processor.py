from typing import Any, List

from ipopy.data_classes.ipo_data_class import IpoDataInfo


def process_ipo_data(ipos_data: List[List[Any]]) -> List[IpoDataInfo]:
    """
    Process IPO data and convert it into a list of IpoDataInfo objects.

    Parameters:
    -----------
        ipos_data: ``List[List[Any]]``
            A list of IPO data, where each inner list contains
            the IPO details in the following order:
            [ipo_name, premium, open_date, close_date, price, allotment_date, listing_date]


    Returns:
    --------
        ``List[IpoDataInfo]``
            A list of IpoDataInfo objects representing the processed IPO data.
    """
    return [
        IpoDataInfo(
            ipo_name=ipo_data[0],
            premium=ipo_data[1],
            open_date=ipo_data[2],
            close_date=ipo_data[3],
            price=ipo_data[4],
            allotment_date=ipo_data[5],
            listing_date=ipo_data[6],
        )
        for ipo_data in ipos_data
    ]

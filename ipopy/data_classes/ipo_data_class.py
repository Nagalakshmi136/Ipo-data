from dataclasses import dataclass


@dataclass
class IpoDataInfo:
    """
    IpoDataInfo dataclass Represents information about IPO.
    """

    ipo_name: str
    premium: str
    open_date: str
    close_date: str
    price: str
    allotment_date: str
    listing_date: str

    def __str__(self) -> str:
        """
        Return a string representation of the IpoDataInfo object.

        Returns:
        --------
            ``str``
                A string representation of the IpoDataInfo object.
        """
        return (
            f"'IPO NAME' : {self.ipo_name},\n"
            f"'PREMIUM' : {self.premium},\n"
            f"'OPEN DATE' : {self.open_date},\n"
            f"'CLOSE DATE' : {self.close_date},\n"
            f"'PRICE' : {self.price},\n"
            f"'ALLOTMENT DATE' : {self.allotment_date},\n"
            f"'LISTING DATE' : {self.listing_date}\n"
        )

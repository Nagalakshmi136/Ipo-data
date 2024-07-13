from pydantic import BaseModel


class IpoDataInfo(BaseModel):
    """
    IpoDataInfo model Represents information about IPO.
    """

    ipo_name: str
    premium: str
    open_date: str | None
    close_date: str | None
    price: str | None
    allotment_date: str | None
    listing_date: str | None

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

from typing import Protocol, Any


class DataFetcherProtocol(Protocol):
    """
    This class represents a data fetcher protocol.

    The `DataFetcherProtocol` class defines the interface for data fetchers.
    Subclasses should implement the `get_data` method to retrieve data for a given target date.
    """

    def get_data(self, target_date: str) -> Any: ...

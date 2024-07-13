from typing import Protocol

class DataSenderProtocol(Protocol):
    """
    This class represents a data sender protocol.

    It defines the interface for sending data.
    """

    def send_data(self) -> None:
        ...
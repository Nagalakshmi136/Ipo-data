from abc import abstractmethod

from registrable import Registrable


class Notifier(Registrable):
    """
    Abstract class for sending notifications to the user.

    Exceptions:
    -----------
    ``NotImplementedError``
        If the method `send_notification` is not implemented.
    """

    @abstractmethod
    def send_notification(self, *args, **kwargs) -> None:
        raise NotImplementedError("Method 'send_notification' must be implemented.")

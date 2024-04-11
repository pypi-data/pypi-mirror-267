"""Local exceptions used by library."""


class ConnectionFailedError(Exception):
    """Thrown when connecting to a processor fails immediately due to an error."""

    def __init__(self, exception):
        message = f"Connection failed: {exception}"
        super().__init__(message)


class ConnectionTimeoutError(Exception):
    """Thrown when connecting to a processor times out."""


class InvalidMacAddressOUIError(Exception):
    """Exception raised for when the Mac address does not start with a valid Trinnov OUI."""

    def __init__(self, mac_oui, valid_ouis):
        valid_ouis_str = ", ".join(valid_ouis)
        self.message = (
            f"Invalid MAC address OUI {mac_oui}, must be one of {valid_ouis_str}"
        )
        super().__init__(self.message)


class MalformedMacAddressError(Exception):
    """Exception raised for malformed MAC addresses."""

    def __init__(self, mac_address, message="Malformed MAC address provided: "):
        self.message = message + mac_address
        super().__init__(self.message)


class NotConnectedError(Exception):
    """Raised when an operation is performed that requires a connect and none is present."""

    def __init__(
        self, message="Not connected to Trinnov Altitude. Did you call `connect()`?"
    ):
        self.message = message
        super().__init__(self.message)

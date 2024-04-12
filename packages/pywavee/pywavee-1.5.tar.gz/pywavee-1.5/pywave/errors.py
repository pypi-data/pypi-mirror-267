from .enums import ErrorSeverity
from discord.enums import try_enum


__all__ = (
    "PywaveError",
    "AuthorizationFailure",
    "LavalinkException",
    "LoadTrackError",
    "BuildTrackError",
    "NodeOccupied",
    "InvalidIDProvided",
    "ZeroConnectedNodes",
    "NoMatchingNode",
    "QueueException",
    "QueueFull",
    "QueueEmpty",
)


class PywaveError(Exception):
    """Base Nextwave Exception"""


class AuthorizationFailure(PywaveError):
    """Exception raised when an invalid password is provided toa node."""


class LavalinkException(PywaveError):
    """Exception raised when an error occurs talking to Lavalink."""


class LoadTrackError(LavalinkException):
    """Exception raised when an error occurred when loading a track."""

    def __init__(self, data):
        exception = data["exception"]
        self.severity: ErrorSeverity
        super().__init__(exception["message"])


class BuildTrackError(LavalinkException):
    """Exception raised when a track is failed to be decoded and re-built."""

    def __init__(self, data):
        super().__init__(data["error"])


class NodeOccupied(PywaveError):
    """Exception raised when node identifiers conflict."""


class InvalidIDProvided(PywaveError):
    """Exception raised when an invalid ID is passed somewhere in Nextwave."""


class ZeroConnectedNodes(PywaveError):
    """Exception raised when an operation is attempted with nodes, when there are None connected."""


class NoMatchingNode(PywaveError):
    """Exception raised when a Node is attempted to be retrieved with a incorrect identifier."""


class QueueException(PywaveError):
    """Base WaveLink Queue exception."""

    pass


class QueueFull(QueueException):
    """Exception raised when attempting to add to a full Queue."""

    pass


class QueueEmpty(QueueException):
    """Exception raised when attempting to retrieve from an empty Queue."""

    pass
"""This logger is used for structured logging in JSON lines."""

import inspect
import logging
from enum import Enum, auto

import structlog
from pythonjsonlogger import jsonlogger
from structlog.types import EventDict

from bookworm.config import config


def get_error_response(
    logger: logging.Logger,  # pylint: disable=unused-argument,redefined-outer-name
    method_name: str,  # pylint: disable=unused-argument
    event_dict: EventDict,
) -> EventDict:
    """This function is used to extract the response text from a non-serializable error."""

    error = event_dict.get("error", None)
    if error and isinstance(error, Exception):
        event_dict["error"] = str(error)

    return event_dict


structlog.configure(
    processors=[
        structlog.processors.TimeStamper(),
        structlog.stdlib.filter_by_level,
        structlog.stdlib.add_logger_name,
        structlog.stdlib.add_log_level,
        get_error_response,
        structlog.stdlib.PositionalArgumentsFormatter(),
        structlog.processors.StackInfoRenderer(),
        structlog.processors.format_exc_info,
        structlog.processors.UnicodeDecoder(),
        structlog.stdlib.render_to_log_kwargs,
    ],
    context_class=dict,
    logger_factory=structlog.stdlib.LoggerFactory(),
    wrapper_class=structlog.stdlib.BoundLogger,
    cache_logger_on_first_use=True,
)

handler = logging.StreamHandler()
handler.setFormatter(jsonlogger.JsonFormatter())
logger = logging.getLogger()
logger.addHandler(handler)
logger.setLevel(config.logging.log_level)


def get_logger():
    """Builds a logger for the calling module.

    The logger will be named after the module that calls this function.

    Returns:
        structlog.BoundLogger: A logger for the calling module
    """
    frm = inspect.stack()[1]
    mod = inspect.getmodule(frm[0])
    return structlog.get_logger(mod.__name__)


class LogEvents(Enum):
    """Log Events for the application."""

    def __str__(self) -> str:
        return self.name

    NFC_DEVICE_NOT_FOUND = auto()
    NFC_DEVICE_INITIALIZED = auto()
    NFC_DEVICE_FAILED = auto()
    NFC_DEVICE_SHUTDOWN = auto()
    NFC_TAG_CONNECTED = auto()
    NFC_TAG_REMOVED = auto()
    NFC_CARD_PRESENT = auto()
    NFC_CARD_REMOVED = auto()
    NFC_TAG_TOO_MANY_NDEF_RECORDS = auto()
    TAG_NO_NDEF_RECORDS = auto()
    TAG_NDEF_RECORD_PRESENT = auto()
    TAG_FILE_DOES_NOT_EXIST = auto()
    STARTUP = auto()
    SIGNAL_RECEIVED = auto()

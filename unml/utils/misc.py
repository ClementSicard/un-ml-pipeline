"""
This module contains miscellaneous functions and classes.
"""

from loguru import logger
from transformers.utils import logging as hfLogging

from unml.utils.consts.logger import LoggerConsts

hfLogging.set_verbosity(40)


def log(
    message: str, verbose: bool, level: str = LoggerConsts.DEFAULT_LOGGER_LEVEL
) -> None:
    """
    Log function to print messages to the console.

    Parameters
    ----------
    `message` : `str`
        The message to be print
    `verbose` : `bool`
        If verbose is `False`, the message won't be printed
    `level` : `str`, optional
        The `loguru` log level, by default DEFAULT_LOGGER_LEVEL
    """

    assert level in LoggerConsts.LOGGER_LEVELS, f"Invalid level: {level}"

    if not verbose:
        return

    match level:
        case "debug":
            logFunc = logger.debug
        case "info":
            logFunc = logger.info
        case "warning":
            logFunc = logger.warning
        case "error":
            logFunc = logger.error
        case "success":
            logFunc = logger.success
        case _:
            logFunc = logger.debug

    logFunc(message)


def isCorrectURL(url: str) -> bool:
    """
    Checks if the given URL is valid.

    Parameters
    ----------
    `url` : `str`
        The URL to be checked

    Returns
    -------
    `bool`
        `True` if the URL is valid, `False` otherwise
    """
    import validators

    return bool(validators.url(url))

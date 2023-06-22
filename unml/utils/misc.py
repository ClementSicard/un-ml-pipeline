"""
This module contains miscellaneous functions and classes.
"""
import inspect
import os
import sys

from loguru import logger
from transformers.utils import logging as hfLogging

from unml.utils.consts.io import IOConsts
from unml.utils.consts.logger import LoggerConsts

hfLogging.set_verbosity(40)


def getPenultimateFunctionName() -> str:
    """
    Get the penultimate function name in the stack.

    Returns
    -------
    `str`
        The penultimate function name in the stack
    """
    # Get the current stack
    stack = inspect.stack()

    # Get the penultimate frame if exists
    if len(stack) >= 3:
        penultimate_frame = stack[2]
        fileName = os.path.relpath(
            penultimate_frame.filename,
            IOConsts.PROJECT_ROOT,
        )
        return f"{fileName}:{penultimate_frame.function}:{penultimate_frame.lineno}"
    else:
        return "N/A"


logger.remove()
logger.add(
    sys.stderr,
    format="<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> | <level>{level: <8}</level>"
    + " | <cyan>{extra[penultimate]}</cyan> | <level>{message}</level>",
    level="DEBUG",
    colorize=True,
    diagnose=False,
    backtrace=False,
)


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

    bindedLogger = logger.bind(penultimate=getPenultimateFunctionName())

    match level:
        case "debug":
            logFunc = bindedLogger.debug
        case "info":
            logFunc = bindedLogger.info
        case "warning":
            logFunc = bindedLogger.warning
        case "error":
            logFunc = bindedLogger.error
        case "success":
            logFunc = bindedLogger.success
        case _:
            logFunc = bindedLogger.debug

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

from loguru import logger

from .consts import DEFAULT_LOGGER_LEVEL, LOGGER_LEVELS


def log(message: str, verbose: bool, level: str = DEFAULT_LOGGER_LEVEL):
    assert level in LOGGER_LEVELS, f"Invalid level: {level}"

    if verbose:
        logger.debug(message)

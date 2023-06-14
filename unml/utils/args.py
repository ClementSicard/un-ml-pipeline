"""
This module contains helpers to parse command line arguments.

Returns
-------
`_type_`
    _description_
"""

from argparse import ArgumentParser
from typing import Any, Dict

from unml.utils.misc import log


def parseArgs() -> Dict[str, Any]:
    """
    Parses the command line arguments.

    Returns
    -------
    `Dict[str, Any]`
        The parsed arguments as a dictionary
    """
    parser = ArgumentParser()

    parser.add_argument("-u", "--url", type=str, required=False)
    parser.add_argument("-f", "--file", type=str, required=False)

    parser.add_argument(
        "-v",
        "--verbose",
        action="store_true",
        default=False,
    )

    parsedArgs = vars(parser.parse_args())

    if not parsedArgs.get("url") and not parsedArgs.get("file"):
        log(
            "You need to specify either a URL or a file. Please try again",
            level="error",
            verbose=True,
        )
        exit()

    if parsedArgs.get("url") and parsedArgs.get("file"):
        log(
            "You specified both a URL and a file. The file will be discarded",
            level="warning",
            verbose=True,
        )
        del parsedArgs["file"]

    return parsedArgs

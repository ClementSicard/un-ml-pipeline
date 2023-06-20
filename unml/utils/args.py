"""
This module contains helpers to parse command line arguments.
"""

from argparse import ArgumentParser
from typing import Any, Dict, List

from loguru import logger

from unml.utils.misc import isCorrectURL, log


class ArgUtils:
    """
    Utility class for CLI arguments related tasks.
    """

    @staticmethod
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
                "You specified both a URL and a file. The URL will be discarded",
                level="warning",
                verbose=True,
            )
            del parsedArgs["url"]

        log(f"Arguments: {parsedArgs}", verbose=parsedArgs["verbose"])

        return parsedArgs

    @staticmethod
    def getURLsFromArgs(args: Dict[str, Any]) -> List[str]:
        """
        Extract a singleton (URL case) or list of paths/urls (file case) depending
        on the CLI arguments.

        Parameters
        ----------
        `args` : `Dict[str, Any]`
            The CLI arguments

        Returns
        -------
        `List[str]`
            The list of paths/URLs
        """
        results = []

        # Case 1: URL CLI arg is specified
        if args.get("url"):
            url: str = args["url"]

            if isCorrectURL(url=url):
                results.append(url)
            else:
                logger.error(f"'{args.get('url')}' is not a valid URL")
                exit()

        # Case 2: file CLI arg is specified
        elif args.get("file"):
            path: str = args["file"]
            try:
                with open(path, "r") as f:
                    for line in f.readlines():
                        if isCorrectURL(line):
                            results.append(line)
                        else:
                            logger.warning(f"'{args.get('url')}' is not a valid URL")

                if not results:
                    logger.error(f"No valid URLs found in {path}.")
                    exit()

            except FileNotFoundError:
                logger.error(f"File '{path}' not found")
                exit()
            except Exception as err:
                logger.error(f"Error while reading file '{path}': {err}")
                exit()

        return results

"""
This module contains helpers to parse command line arguments.
"""

from argparse import ArgumentParser
from typing import Any, Dict, List

from unml.utils.api import APIUtils
from unml.utils.consts.ner import NERConsts
from unml.utils.consts.summarize import SummarizationConsts
from unml.utils.misc import log


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
            "-o",
            "--output",
            type=str,
            help="Output file path",
            required=False,
            default="output.json",
        )

        parser.add_argument(
            "-v",
            "--verbose",
            action="store_true",
            help="Verbose mode",
            default=False,
        )

        parser.add_argument(
            "--summarize",
            action="store_true",
            default=False,
            help="Summarize the text if set",
        )
        parser.add_argument(
            "--ner",
            action="store_true",
            default=False,
            help="Perform NER on the text if set",
        )

        parser.add_argument(
            "--summarizer",
            type=str,
            default=SummarizationConsts.DEFAULT_SUMMARIZATION_MODEL,
            choices=SummarizationConsts.ARGS_MAP.keys(),
            help="Model to use for summarization",
        )
        parser.add_argument(
            "--recognizer",
            type=str,
            default=NERConsts.DEFAULT_NER_MODEL,
            choices=NERConsts.ARGS_MAP.keys(),
            help="Model to use for NER",
        )

        parsedArgs = vars(parser.parse_args())

        if not parsedArgs.get("summarize"):
            parsedArgs["summarizer"] = None

        if not parsedArgs.get("ner"):
            parsedArgs["recognizer"] = None

        # Error: no URL or file specified
        if not parsedArgs.get("url") and not parsedArgs.get("file"):
            log(
                "You need to specify either a URL or a file. Please try again",
                level="error",
                verbose=True,
            )
            exit(1)

        # Warning: both URL and file specified. Only file will be used
        if parsedArgs.get("url") and parsedArgs.get("file"):
            log(
                "You specified both a URL and a file. The URL will be discarded",
                level="warning",
                verbose=True,
            )
            del parsedArgs["url"]

        # Error: In case none of ner or summarize is specified
        if not parsedArgs.get("ner") and not parsedArgs.get("summarize"):
            log(
                "You need to specify either --ner or --summarize. Please try again",
                level="error",
                verbose=True,
            )
            exit(1)

        log(f"Arguments: {parsedArgs}", verbose=True)

        return parsedArgs

    @staticmethod
    def getURLsAndIDsFromArgs(args: Dict[str, Any]) -> List[str]:
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

            if APIUtils.isCorrectURL(url=url):
                results.append(url)
            else:
                log(
                    f"'{args.get('url')}' is not a valid URL",
                    level="error",
                    verbose=True,
                )
                exit(1)

        # Case 2: file CLI arg is specified
        elif args.get("file"):
            path: str = args["file"]
            try:
                with open(path, "r") as f:
                    for line in f.readlines():
                        line = line.strip()

                        if line.startswith("#"):
                            continue

                        if APIUtils.isCorrectURL(line):
                            results.append(line)
                        else:
                            log(
                                f"'{line}' is not a valid URL. Skipping.",
                                level="warning",
                                verbose=True,
                            )

                if not results:
                    log(
                        f"No valid URLs found in {path}.",
                        level="error",
                        verbose=True,
                    )
                    exit(1)

            except FileNotFoundError:
                log(
                    f"File '{path}' not found",
                    level="error",
                    verbose=True,
                )
                exit(1)
            except Exception as err:
                log(
                    f"Error while reading file '{path}': {err}",
                    level="error",
                    verbose=True,
                )
                exit(1)

        log(f"Number of URLs: {len(results)}", verbose=True, level="success")
        return results

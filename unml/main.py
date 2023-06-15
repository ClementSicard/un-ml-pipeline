from typing import Any, Dict

from unml.modules.summarize import Summarizer
from unml.utils.args import parseArgs
from unml.utils.misc import log
from unml.utils.text import getDocumentText


def runPipielines(args: Dict[str, Any]) -> None:
    """
    Main function to run subpipelines: get text from URL, summarize text, etc.

    Parameters
    ----------
    `args` : `Dict[str, Any]`
        The parsed CLI arguments as a dictionary
    """
    text = getDocumentText(url=args["url"])

    log(f"Text: {text}", verbose=args["verbose"])

    summarizer = Summarizer()
    summary = summarizer.summarize(text=text)

    log(f"Summary: {summary}", verbose=args["verbose"])


if __name__ == "__main__":
    args = parseArgs()
    log(f"Arguments: {args}", verbose=args["verbose"])

    runPipielines(args=args)

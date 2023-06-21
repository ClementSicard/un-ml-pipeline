from typing import List

from unml.modules.summarize import Summarizer
from unml.utils.args import ArgUtils
from unml.utils.misc import log
from unml.utils.network import NetworkUtils


def runPipielines(urls: List[str], verbose: bool = False) -> None:
    """
    Main function to run subpipelines: get text from a batch of URLs, then summarize
    text, extract Named Entities...

    Parameters
    ----------
    `urls` : `List[str]`
        List of document URLs
    `verbose` : `bool`, optional
        Controls the verbose of the output, by default False
    """

    texts = NetworkUtils.extractTextFromURLs(urls=urls, verbose=verbose)

    for textJson in texts:
        text = textJson["text"]
        if text is not None:
            log(
                f"Text: {text[:1000] + '...' if len(text) > 1000 else text}",
                verbose=verbose,
            )

            log(f"Document size: {len(text)} characters", verbose=verbose)
            summarizer = Summarizer()
            summary = summarizer.summarize(text=text, verbose=verbose)

            log(f"Summary: {summary}", verbose=verbose)
        else:
            log(
                f"Extracted text for {textJson['url']} is empty!",
                level="error",
                verbose=verbose,
            )


if __name__ == "__main__":
    args = ArgUtils.parseArgs()
    urls = ArgUtils.getURLsFromArgs(args=args)

    runPipielines(urls=urls, verbose=args["verbose"])

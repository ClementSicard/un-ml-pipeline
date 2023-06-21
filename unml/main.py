from typing import List

from tqdm import tqdm

from unml.modules.ner import NamedEntityRecognizer
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

    """
    1. Get text from files corresponding to URLs
    """
    summarizer = Summarizer()
    ner = NamedEntityRecognizer()

    texts = NetworkUtils.extractTextFromURLs(urls=urls, verbose=verbose)

    for textJson in tqdm(texts) if not verbose else texts:
        text = textJson["text"]
        if text is not None:
            log(
                f"Text: {text[:1000] + '...' if len(text) > 1000 else text}",
                verbose=verbose,
            )

            log(f"Document size: {len(text)} characters", verbose=verbose)

            """
            2. Summarize text
            """
            summary = summarizer.summarize(text=text, verbose=verbose)
            log(f"Summary: {summary}", verbose=verbose)

            """
            3. Named Entity Recognition
            """
            ner.recognize(text=text, verbose=verbose)

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

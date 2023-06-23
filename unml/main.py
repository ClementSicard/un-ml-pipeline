from typing import List

from tqdm import tqdm

from unml.modules.ner import NamedEntityRecognizer
from unml.modules.summarize import Summarizer
from unml.utils.args import ArgUtils
from unml.utils.io import IOUtils
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
    0. Instantiate summarizer and NER depending on tasks
    """
    if args["summarize"]:
        summarizer = Summarizer(model=args["summarizer"])
    if args["ner"]:
        ner = NamedEntityRecognizer()

    """
    1. Get text from files corresponding to URLs
    """

    texts = NetworkUtils.extractTextFromURLs(urls=urls, verbose=verbose)
    results = []

    for textJson in tqdm(texts) if not verbose else texts:
        text = textJson["text"]
        result = {
            "url": textJson["url"],
            "summary": None,
            "named_entities": {
                "list": None,
                "detailed": None,
            },
        }

        if text is not None:
            log(f"Document size: {len(text)} characters", verbose=verbose)
            log(
                f"Text: {text[:1000] + '...' if len(text) > 1000 else text}",
                verbose=verbose,
            )

            """
            2. Summarize text
            """
            if args["summarize"]:
                summary = summarizer.summarize(text=text, verbose=verbose)
                log(f"Summary: {summary}", verbose=verbose)
                result["summary"] = summary

            """
            3. Named Entity Recognition
            """
            if args["ner"]:
                entities, detailed = ner.recognizeFromChunked(
                    text=text, verbose=verbose
                )
                result["named_entities"]["list"] = entities
                result["named_entities"]["detailed"] = detailed

            results.append(result)

        else:
            log(
                f"Extracted text for {textJson['url']} is empty!",
                level="error",
                verbose=verbose,
            )

    # Save results to a JSON file
    IOUtils.saveResults(results=results, path=args["output"])

    log("Done!", level="success", verbose=verbose)


if __name__ == "__main__":
    args = ArgUtils.parseArgs()
    urls = ArgUtils.getURLsFromArgs(args=args)

    runPipielines(urls=urls, verbose=args["verbose"])

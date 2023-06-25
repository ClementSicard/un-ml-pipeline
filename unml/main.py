import sys
from typing import Any, Dict, List

from tqdm import tqdm

from unml.modules.ner import NamedEntityRecognizer
from unml.modules.summarize import Summarizer
from unml.utils.api import APIUtils
from unml.utils.args import ArgUtils
from unml.utils.io import IOUtils
from unml.utils.misc import log
from unml.utils.network import NetworkUtils
from unml.utils.types.document import Document
from unml.utils.types.json import JSON


def runPipelines(docs: List[Document], args: Dict[str, Any]) -> List[JSON]:
    """
    Main function to run subpipelines: get text from a batch of URLs, then summarize
    text, extract Named Entities...

    Parameters
    ----------
    `docs` : `List[Document]`
        List of `Document` objects to run the pipeline on
    `verbose` : `bool`, optional
        Controls the verbose of the output, by default False

    Returns
    -------
    `List[JSON]`:
        The list of documents with the pipeline results
    """
    verbose = args["verbose"]
    """
    0. Instantiate summarizer and NER depending on tasks
    """
    if args["summarize"]:
        summarizer = Summarizer(model=args["summarizer"])
    if args["ner"]:
        ner = NamedEntityRecognizer(model=args["recognizer"])

    """
    1. Get text from files corresponding to URLs
    """

    texts = NetworkUtils.extractTextFromDocuments(docs=docs, verbose=verbose)
    results: List[JSON] = []

    for textJson in tqdm(texts) if not verbose else texts:
        print("=" * 100 + "\n", file=sys.stderr)
        log(f"Started working on {textJson['url']}", verbose=verbose, level="warning")
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
                result["summary"] = summarizer.summarize(text=text, verbose=verbose)

            """
            3. Named Entity Recognition
            """
            if args["ner"]:
                entities, detailed = ner.recognize(
                    text=text,
                    verbose=verbose,
                )
                result["named_entities"]["list"] = entities
                result["named_entities"]["detailed"] = detailed

            """
            4. Save results
            """
            results.append(result)

        else:
            log(
                f"Extracted text for {textJson['url']} is empty!",
                level="error",
                verbose=verbose,
            )

    # Save results to a JSON file
    if args.get("output"):
        IOUtils.saveResults(results=results, path=args["output"])

    log("Done!", level="success", verbose=verbose)

    return results


if __name__ == "__main__":
    args = ArgUtils.parseArgs()
    urls = ArgUtils.getURLsAndIDsFromArgs(args=args)

    docs = [
        Document(url=url, recordId=APIUtils.extractRecordIdFromURL(url=url))
        for url in urls
    ]

    log(f"Documents: {docs}", verbose=args["verbose"])

    runPipelines(
        docs=docs,
        args=args,
    )

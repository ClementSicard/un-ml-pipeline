import sys
from typing import Any, Dict, List

from tqdm import tqdm

from unml.graphdb.graphdb import GraphDB
from unml.modules.ner import NamedEntityRecognizer
from unml.modules.summarize import Summarizer
from unml.utils.api import APIUtils
from unml.utils.args import ArgUtils
from unml.utils.io import IOUtils
from unml.utils.misc import log
from unml.utils.network import NetworkUtils
from unml.utils.types.document import Document
from unml.utils.types.json import JSON


def runPipelines(
    docs: List[Document],
    args: Dict[str, Any],
) -> List[JSON]:
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
    0. Instantiate summarizer and NER depending on tasks as well as GraphDB connector
    """
    graphDB = GraphDB()
    graphDB.checkConnection()

    if args["summarize"]:
        summarizer = Summarizer(model=args["summarizer"])
    if args["ner"]:
        ner = NamedEntityRecognizer(model=args["recognizer"])

    """
    1. Get text from files corresponding to URLs
    """

    texts = NetworkUtils.extractTextFromDocuments(docs=docs, verbose=verbose)
    results: List[JSON] = []

    assert len(texts) == len(
        docs
    ), f"Length of texts and docs is not equal! {len(texts)} texts != {len(docs)} docs"

    for textJson, doc in tqdm(zip(texts, docs)) if not verbose else zip(texts, docs):
        print("=" * 100 + "\n", file=sys.stderr)
        log(f"Started working on {textJson['url']}", verbose=verbose, level="warning")
        extractedText = textJson["text"]

        # Initialize result JSON
        result: JSON = {
            "url": textJson["url"],
            "summary": None,
            "named_entities": {
                "list": None,
                "detailed": None,
            },
        }

        if extractedText is not None:
            log(f"Document size: {len(extractedText)} characters", verbose=verbose)
            log(
                f"Text: {extractedText}",
                verbose=verbose,
            )

            """
            2. Summarize text
            """
            if args["summarize"]:
                result["summary"] = summarizer.summarize(
                    text=extractedText, verbose=verbose
                )
                doc.summary = result["summary"]

            """
            3. Named Entity Recognition
            """
            if args["ner"]:
                entities, countries, detailed = ner.recognize(
                    text=extractedText,
                    verbose=verbose,
                )
                result["named_entities"]["list"] = entities
                result["named_entities"]["countries"] = countries
                result["named_entities"]["detailed"] = detailed

            """
            4. Save results to result array
            """
            results.append(result)

            """
            5. Save results to GraphDB
            """
            graphDB.createDocument(doc=doc, verbose=verbose)

        else:
            log(
                f"Extracted text for {textJson['url']} is empty!",
                level="error",
                verbose=verbose,
            )

    # Save results to a JSON file
    if args.get("output"):
        IOUtils.saveResults(results=results, path=args["output"])

    log("Done!", level="success", verbose=True)

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

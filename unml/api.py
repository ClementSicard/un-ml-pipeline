import os
from typing import Dict, List, Optional

from fastapi import FastAPI, HTTPException
from loguru import logger
from tqdm import tqdm
from undl.client import UNDLClient

from unml.graphdb.graphdb import GraphDB
from unml.main import runPipelines
from unml.utils.consts.api import APIConsts
from unml.utils.misc import log
from unml.utils.network import NetworkUtils
from unml.utils.types.document import Document
from unml.utils.types.json import JSON
from unml.utils.types.record import Record

clientUNDL = UNDLClient(verbose=False)
graphDB = GraphDB()

recordsCache: Dict[str, Optional[Document]] = {}


def onStart() -> None:
    """
    Function to run on startup.
    """
    log("Starting API...", level="info", verbose=True)
    graphDB.checkConnection()

    if os.getenv("UN_API") is None:
        raise ValueError("Environment variable UN_API is not set!")

    log("API started!", level="success", verbose=True)


app = FastAPI(
    debug=True,
    title="UNML API",
    description="API for the machine learning pipeline of the UNML project",
    # When the API starts, check the connection to the GraphDB
    on_startup=[onStart],
)


@app.get("/")  # type: ignore
def readRoot() -> JSON:
    """
    Root endpoint.

    Returns
    -------
    `JSON`
        A simple JSON object with a `"Hello"` key and a `"World"` value
    """
    return {"Hello": "✅"}


@app.post("/run")  # type: ignore
def run(records: List[Record], n: int = 400) -> JSON | List[JSON]:
    """
    Post a list of record IDs to run the pipeline on the documents
    corresponding to them.

    The pipeline is run with the default arguments, defined in `APIConsts` in
    `unml/utils/consts/api.py`.

    Parameters
    ----------
    `docs` : `List[Record]`
        The list of record IDs
    `n`: `int`
        The number of documents to return. Defaults to `400`.

    Returns
    -------
    `JSON | List[JSON]`
        The list of documents with the pipeline results
    """

    currentRecord = ""
    nonExistentRecords = [
        record
        for record in tqdm(records, desc="Checking if records exist...", unit="record")
        if not graphDB.docExists(record)
    ]
    log(
        f"{len(records) - len(nonExistentRecords):,} documents are already in the DB.",
        verbose=True,
    )
    try:
        parsedDocs = []

        for record in nonExistentRecords[:n]:
            currentRecord = record.recordId
            if graphDB.docExists(record):
                log(
                    f"Record {record.recordId} found in GraphDB!",
                    verbose=True,
                    level="success",
                )
                continue
            elif record.recordId in recordsCache:
                log(
                    f"Record {record.recordId} found in cache!",
                    verbose=True,
                    level="success",
                )
                parsedDocs.append(recordsCache[record.recordId])
                continue

            doc = NetworkUtils.queryByIdUNDL(record=record)
            parsedDocs.append(doc)
            recordsCache[record.recordId] = doc

    except Exception as e:
        log(f"Error: {e} at record {currentRecord}", level="error", verbose=True)
        raise HTTPException(500, f"Internal server error: {e}")

    if len(parsedDocs) == 0:
        return {
            "info": "No new documents found",
        }
    return runPipelines(documents=parsedDocs, args=APIConsts.DEFAULT_PIPELINE_ARGS)


@app.get("/run_search")  # type: ignore
def run_search(q: str, n: int = 400) -> JSON | List[JSON]:
    """
    Get a prompt to run the pipeline on all the documents
    corresponding to the response of the corresponding search.

    The function first get all the IDs of all the documents corresponding to the search,
    then runs the pipeline on them.

    The pipeline is run with the default arguments, defined in `APIConsts` in
    `unml/utils/consts/api.py`.

    Parameters
    ----------
    `q` : `str`
        The prompt to search for
    `n`: `int`
        The number of documents to return. Defaults to `400`.

    Returns
    -------
    `List[JSON]`
        The list of documents with the pipeline results
    """

    logger.info(f"Querying UNDL for prompt: {q}")

    results = clientUNDL.getAllRecordIds(prompt=q)
    ids = results["hits"]
    records = [Record(recordId=id_) for id_ in ids]

    log(
        f"{len(records):,} records are associated with search '{q}'",
        level="success",
        verbose=True,
    )

    runResult: JSON | List[JSON] = run(records=records)

    return runResult

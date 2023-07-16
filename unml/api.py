import json
from typing import List

from fastapi import FastAPI, HTTPException
from undl.client import UNDLClient

from unml.graphdb.graphdb import GraphDB
from unml.main import runPipelines
from unml.utils.consts.api import APIConsts
from unml.utils.misc import log
from unml.utils.types.document import Document
from unml.utils.types.json import JSON
from unml.utils.types.record import Record

clientUNDL = UNDLClient(verbose=True)
graphDB = GraphDB()

app = FastAPI(
    debug=True,
    title="UNML API",
    description="API for the machine learning pipeline of the UNML project",
    # When the API starts, check the connection to the GraphDB
    on_startup=[graphDB.checkConnection],
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
    return {"Hello": "World"}


@app.post("/run")  # type: ignore
def run(records: List[Record]) -> List[JSON]:
    """
    Post a list of record IDs to run the pipeline on the documents
    corresponding to them.

    The pipeline is run with the default arguments, defined in `APIConsts` in
    `unml/utils/consts/api.py`.

    Parameters
    ----------
    `docs` : `List[Record]`
        The list of record IDs

    Returns
    -------
    `List[JSON]`
        The list of documents with the pipeline results
    """
    parsedDocs = []

    for record in records:
        # 1. Query the API with the record ID to get the document info
        queryResult = clientUNDL.queryById(recordId=record.recordId)
        log(
            json.dumps(queryResult, indent=4, ensure_ascii=False),
            verbose=True,
            level="debug",
        )
        try:
            # 2. Create a document object from the API response
            doc = Document.fromLibraryAPIResponse(response=queryResult["records"][0])
            parsedDocs.append(doc)

        except KeyError as e:
            log(f"Error: {e}", level="error", verbose=True)

            # Error: no URL or file specified
            if "English" not in e.args[0]:
                raise HTTPException(
                    status_code=404,
                    detail=f"No URL found for id '{record.recordId}'",
                )
            else:
                raise HTTPException(status_code=500, detail="Internal server error")

        except Exception as e:
            log(f"Error: {e}", level="error", verbose=True)
            # Error: no URL or file specified
            raise HTTPException(status_code=500, detail="Internal server error")

    return runPipelines(docs=parsedDocs, args=APIConsts.DEFAULT_PIPELINE_ARGS)

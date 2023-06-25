from typing import List

from fastapi import FastAPI, HTTPException
from undl.client import UNDLClient

from unml.main import runPipelines
from unml.utils.consts.api import APIConsts
from unml.utils.misc import log
from unml.utils.types.document import Document, QueryDocument
from unml.utils.types.json import JSON

app = FastAPI(
    debug=True,
    title="UNML API",
    description="API for the machine learning pipeline of the UNML project",
)


@app.get("/")
def readRoot() -> JSON:
    """
    Root endpoint.

    Returns
    -------
    `JSON`
        A simple JSON object with a `"Hello"` key and a `"World"` value
    """
    return {"Hello": "World"}


@app.post("/run")
def run(queryDocs: List[QueryDocument]) -> List[JSON]:
    """
    Post a list of documents to run the pipeline on.

    Parameters
    ----------
    `docs` : `List[QueryDocument]`
        The list of documents to run the pipeline on

    Returns
    -------
    `List[JSON]`
        The list of documents with the pipeline results
    """
    for doc in queryDocs:
        if doc.url is None:
            client = UNDLClient(verbose=True)
            queryResult = client.queryById(
                recordId=doc.recordId,
                oldURL=True,
                outputFormat="marcxml",
            )
            try:
                url = queryResult[0]["downloads"]["English"]
                doc.url = url

            except KeyError as e:
                log(f"Error: {e}", level="error", verbose=True)
                # Error: no URL or file specified
                raise HTTPException(
                    status_code=404, detail=f"No URL found for id {doc.recordId}"
                )
            except Exception as e:
                log(f"Error: {e}", level="error", verbose=True)
                # Error: no URL or file specified
                raise HTTPException(status_code=500, detail="Internal server error")

            log(f"Query result: {queryResult}", verbose=True)

    docs: List[Document] = [Document(**doc.dict()) for doc in queryDocs]

    return runPipelines(docs=docs, args=APIConsts.DEFAULT_PIPELINE_ARGS)

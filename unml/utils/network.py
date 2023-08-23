import asyncio
import os
import time
from typing import Any, Dict, List, Optional

import aiohttp
from requests import get
from undl.client import UNDLClient

from unml.utils.consts.io import IOConsts
from unml.utils.io import IOUtils
from unml.utils.misc import log
from unml.utils.text import TextUtils
from unml.utils.types.document import Document
from unml.utils.types.record import Record


class NetworkUtils:
    """
    Utility class for network related tasks.
    """

    def downloadSingleDocument(
        self,
        url: str,
        output: Optional[str] = None,
        verbose: bool = False,
    ) -> str:
        """
        Download a document from a given URL.

        Parameters
        ----------
        `url` : `str`
            The URL of the document
        `output` : `Optional[str]`, optional
            Output destination, by default None
        `verbose` : `bool`
            The verbose argument. Defaults to `False`.

        Returns
        -------
        `str`
            The path to the downloaded document
        """
        log(f"Downloading document from {url}...", level="info", verbose=verbose)

        if output is None:
            fileName = url.split("/")[-1]
            os.makedirs(IOConsts.DOWNLOADS_FOLDER, exist_ok=True)
            output = os.path.join(IOConsts.DOWNLOADS_FOLDER, fileName)

        with open(output, "wb") as f:
            f.write(get(url).content)

        log(f"Document downloaded to {output}!", level="success", verbose=verbose)

        return output

    @staticmethod
    def extractTextFromDocuments(
        docs: List[Document],
        headers: Optional[Dict[str, Any]] = None,
        verbose: bool = False,
    ) -> List[Dict[str, str]]:
        """
        Downloads document corresponding to URLs and extracts the text
        out of them.

        Parameters
        ----------
        `docs` : `List[Document]`
            The list of documents
        `headers` : `Optional[Dict[str, Any]]`, optional
            The headers to pass to the HTTP request, by default `None`
        `verbose` : `bool`, optional
            Controls the verbose, by default `False`


        Returns
        -------
        `List[Dict[str, str]]`
            A list of dictionnaries, containing `"url"` and `"text"` fields.
        """

        start = time.time()
        results = asyncio.run(
            NetworkUtils.getExtractedTextFromMultipleURLs(
                urls=[doc.url for doc in docs if doc.url is not None],
                headers=headers,
                verbose=verbose,
            )
        )

        end = time.time()

        if verbose:
            log(
                f"Took {end-start:.2f} seconds to download {len(docs)} urls!",
                level="success",
                verbose=verbose,
            )

        return results

    @staticmethod
    async def getExtractedTextFromURL(
        url: str,
        session: aiohttp.ClientSession,
        headers: Optional[Dict[str, Any]] = None,
        verbose: bool = False,
    ) -> Dict[str, str | None]:
        """
        Wrapper around an async HTTP GET request. The response is then parsed,
        the text extracted and cleaned.

        Parameters
        ----------
        `url` : `str`
            The URL to get
        `session` : `aiohttp.ClientSession`
            The `aiohttp` session
        `headers` : `Optional[Dict[str, Any]]`, optional
            Headers to pass to the request, by default `None`
        `toJson` : `bool`, optional
            If `True`, the output will be of the form `{"url": "...", "text": "..."}`.
            By default `False`
        `verbose` : `bool`, optional
            Controls the verbose, by default `False`

        Returns
        -------
        `Dict[str, str | None] | None`
            The text content of file corresponding to the URL. `None` if there was an issue
        """
        try:
            async with session.get(url=url, headers=headers) as response:
                resp = await response.read()

                savedFilePath = IOUtils.saveFileToDownloads(
                    fileName=url.split("/")[-1],
                    content=resp,
                )

                if savedFilePath is not None:
                    extractedText: str = TextUtils.extractTextFromFile(
                        path=savedFilePath,
                        verbose=verbose,
                    )
                    cleanedText = TextUtils.cleanText(text=extractedText)
                else:
                    cleanedText = None

                return {"url": url, "text": cleanedText}

        except Exception as e:
            log(f"Unable to get url {url} due to {e}.", level="error", verbose=verbose)

            return {"url": url, "text": None}

    @staticmethod
    async def getExtractedTextFromMultipleURLs(
        urls: List[str],
        headers: Optional[Dict[str, Any]] = None,
        verbose: bool = False,
    ) -> List[Dict[str, str]]:
        """
        Helper function to download multiple URLs asynchronously.

        Parameters
        ----------
        `urls` : `List[str]`
            List of URLs to download
        `headers` : `Optional[Dict[str, Any]]`, optional
            Headers to pass to the request, by default `None`
        `verbose` : `bool`, optional
            Verbose argument, by default `False`

        Returns
        -------
        `List[Dict[str, str]]`
            The contents of the given URLs, in the form of a list of
            `{"url": "...", "text": "..."}` objects.
        """
        async with aiohttp.ClientSession() as session:
            ret = await asyncio.gather(
                *[
                    NetworkUtils.getExtractedTextFromURL(
                        url=url,
                        session=session,
                        headers=headers,
                    )
                    if url is not None
                    else {"url": None, "text": None}
                    for url in urls
                ]
            )

        log(
            f"Finalized all. Return is a list of len {len(ret)} outputs.",
            level="success",
            verbose=verbose,
        )

        return ret

    @staticmethod
    def queryByIdUNDL(record: Record) -> Optional[Document]:
        """
        Query the UNDL API with a given record ID.

        Parameters
        ----------
        `record` : `Record`
            The record to query the API with

        Returns
        -------
        `Optional[Document]`
            The document corresponding to the record ID, `None` if not found or doesn't contain the right structure.
        """
        clientUNDL = UNDLClient(verbose=True)

        queryResult = clientUNDL.queryById(recordId=record.recordId)

        if len(queryResult["records"]) == 0:
            return None
        # 2. Create a document object from the API response
        doc = Document.fromLibraryAPIResponse(
            response=queryResult["records"][0]
            if len(queryResult["records"]) > 0
            else {},
            acceptNoDownloads=True,
        )

        return doc

import asyncio
import os
import time
from typing import Any, Dict, List, Optional

import aiohttp
from requests import get

from unml.utils.consts import DOWNLOADS_FOLDER
from unml.utils.io import IOUtils
from unml.utils.misc import log
from unml.utils.text import TextUtils


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
            file_name = url.split("/")[-1]
            os.makedirs(DOWNLOADS_FOLDER, exist_ok=True)
            output = os.path.join(DOWNLOADS_FOLDER, file_name)

        with open(output, "wb") as f:
            f.write(get(url).content)

        log(f"Document downloaded to {output}!", level="success", verbose=verbose)

        return output

    @staticmethod
    def extractTextFromURLs(
        urls: List[str],
        headers: Optional[Dict[str, Any]] = None,
        verbose: bool = False,
    ) -> List[Dict[str, str]]:
        """
        Downloads document corresponding to URLs and extracts the text
        out of them.

        Parameters
        ----------
        `urls` : `List[str]`
            The list of URLs
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
            NetworkUtils.downloadMultipleURLs(
                urls=urls,
                headers=headers,
                verbose=verbose,
                toJson=True,  # True --> {"url": "...", "text": "..."}
            )
        )

        end = time.time()

        if verbose:
            log(
                f"Took {end-start:.2f} seconds to download {len(urls)} urls!",
                level="success",
                verbose=verbose,
            )

        return results

    @staticmethod
    async def get(
        url: str,
        session: aiohttp.ClientSession,
        headers: Optional[Dict[str, Any]] = None,
        toJson: bool = False,
        verbose: bool = False,
    ) -> str | Dict[str, str | None] | None:
        """
        Wrapper around an async HTTP GET request

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
        `str | Dict[str, str | None] | None`
            The text content of the URL. `None` if there was an issue
        """
        try:
            async with session.get(url=url, headers=headers) as response:
                resp = await response.read()

                log(f"Response type: {type(resp)}", verbose=True)

                savedFilePath = IOUtils.saveFile(
                    fileName=url.split("/")[-1],
                    content=resp,
                )

                extractedText: str = TextUtils.extractTextFromFile(path=savedFilePath)

                if toJson:
                    return {"url": url, "text": extractedText}

                return extractedText
        except Exception as e:
            log(f"Unable to get url {url} due to {e}.", level="error", verbose=verbose)
            if toJson:
                return {"url": url, "text": None}

            return None

    @staticmethod
    async def downloadMultipleURLs(
        urls: List[str],
        headers: Optional[Dict[str, Any]] = None,
        verbose: bool = False,
        toJson: bool = False,
    ) -> List[Dict[str, str]] | List[str]:
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
        `List[str | Dict[str, str]]`
            The contents of the given URLs
        """
        async with aiohttp.ClientSession() as session:
            ret = await asyncio.gather(
                *[
                    NetworkUtils.get(
                        url=url,
                        session=session,
                        headers=headers,
                        toJson=toJson,
                    )
                    for url in urls
                ]
            )

        log(
            f"Finalized all. Return is a list of len {len(ret)} outputs.",
            level="success",
            verbose=verbose,
        )

        return ret

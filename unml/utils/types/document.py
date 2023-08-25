from typing import Any, Dict, List, Optional

from pydantic import BaseModel

from unml.utils.misc import log
from unml.utils.text import TextUtils


class Document(BaseModel):  # type: ignore
    """
    This class models a document.
    """

    recordId: str
    title: str
    url: Optional[str] = None
    altTitle: Optional[str] = None
    location: Optional[str] = None
    symbol: Optional[str] = None
    subjects: Optional[List[str]] = None
    publicationDate: Optional[str] = None
    relatedDocuments: Optional[List["Document"]] = None
    unBodies: Optional[List[str]] = None
    countries: Optional[List[str]] = None
    summary: Optional[str] = None
    namedEntities: Optional[Dict[str, Dict[str, int] | List[Dict[str, Any]]]] = None

    def toGraphDBObject(self) -> str:
        """
        Convert the document to a Cypher query.
        The list of subjects is ignored to avoid duplicates
        with the links.

        Returns
        -------
        `str`
            The Cypher object for the document.

        Example
        --------
        ```python
        >>> doc = Document(
        ...     recordId="A/RES/75/1",
        ...     title="The situation in the Middle East",
        ...     altTitle="The situation in the Middle East",
        ...     location="New York",
        ...     symbol="A/RES/75/1",
        ...     publicationDate="2020-09-15",
        ...     summary="The situation in the Middle East",
        ...     url="https://undocs.org/A/RES/75/1",
        ... )
        >>> doc.toGraphDBObject()
        'p:Document {
            id: "A/RES/75/1",
            title: "The situation in the Middle East",
            altTitle: "The situation in the Middle East",
            location: "New York",
            symbol: "A/RES/75/1",
            publicationDate: "2020-09-15",
            summary: "The situation in the Middle East",
            url: "https://undocs.org/A/RES/75/1"
        }'
        ```
        """
        return """d:Document
            {{
                id: "{recordId}",
                title: "{title}",
                altTitle: "{altTitle}",
                location: "{location}",
                symbol: "{symbol}",
                publicationDate: "{publicationDate}",
                summary: "{summary}",
                url: "{url}"
            }}
        """.format(
            recordId=TextUtils.replaceIfNotNull(self.recordId, '"', '\\"'),
            title=TextUtils.replaceIfNotNull(self.title, '"', '\\"'),
            altTitle=TextUtils.replaceIfNotNull(self.altTitle, '"', '\\"'),
            location=TextUtils.replaceIfNotNull(self.location, '"', '\\"'),
            symbol=TextUtils.replaceIfNotNull(self.symbol, '"', '\\"'),
            publicationDate=TextUtils.replaceIfNotNull(
                self.publicationDate, '"', '\\"'
            ),
            summary=TextUtils.replaceIfNotNull(self.summary, '"', '\\"'),
            url=TextUtils.replaceIfNotNull(self.url, '"', '\\"'),
        )

    @classmethod
    def fromLibraryAPIResponse(
        cls,
        response: Dict[str, Any],
        acceptNoDownloads: bool = True,
    ) -> "Document":
        """
        Parse the information from the response of the UNDL API.

        Parameters
        ----------
        `response` : `Dict[str, Any]`
            Response of the UNDL API

        Returns
        -------
        `Document`
            The parsed document.
        """
        downloads = response.get("downloads")
        subjects = response.get("subjects")

        if (
            downloads is None or downloads.get("English") is None
        ) and not acceptNoDownloads:
            log("No downloads found in the response", level="warning", verbose=True)

        return cls(
            recordId=response["id"],
            title=response["title"],
            url=downloads.get("English") if downloads else None,
            altTitle=response.get("altTitle"),
            location=response.get("location"),
            symbol=response.get("symbol"),
            publicationDate=response.get("publicationDate"),
            subjects=subjects["unbist"] if subjects else [],
            relatedDocuments=response.get("relatedDocuments"),
            unBodies=response.get("unBodies"),
        )

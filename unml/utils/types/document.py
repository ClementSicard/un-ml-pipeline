from typing import Any, Dict, List, Optional

from pydantic import BaseModel


class QueryDocument(BaseModel):  # type: ignore
    """
    This class models a potentially incomplete document.
    """

    recordId: str
    title: str
    url: Optional[str] = None
    summary: Optional[str] = None
    namedEntities: Optional[Dict[str, Dict[str, int] | List[Dict[str, Any]]]] = None


class Document(BaseModel):  # type: ignore
    """
    This class models a document.
    """

    recordId: str
    title: str
    url: str
    summary: Optional[str] = None
    namedEntities: Optional[Dict[str, Dict[str, int] | List[Dict[str, Any]]]] = None

    def toParams(self) -> Dict[str, Any]:
        """
        Convert the document to a dictionary of parameters.

        Returns
        -------
        `Dict[str, Any]`
            The dictionary of parameters
        """
        return {
            "id": self.recordId,
            "title": self.title,
            "summary": self.summary,
            "url": self.url,
        }

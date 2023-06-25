from typing import Any, Dict, List, Optional

from pydantic import BaseModel


class QueryDocument(BaseModel):  # type: ignore
    """
    This class models a potentially incomplete document.
    """

    recordId: str
    url: Optional[str] = None
    summary: Optional[str] = None
    namedEntities: Optional[Dict[str, Dict[str, int] | List[Dict[str, Any]]]] = None


class Document(BaseModel):  # type: ignore
    """
    This class models a document.
    """

    recordId: str
    url: str
    summary: Optional[str] = None
    namedEntities: Optional[Dict[str, Dict[str, int] | List[Dict[str, Any]]]] = None

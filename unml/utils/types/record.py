from pydantic import BaseModel


class Record(BaseModel):  # type: ignore
    """
    This class models a record, by unique id `recordId`.

    This value is taken from UN Digital Library API.
    """

    recordId: str

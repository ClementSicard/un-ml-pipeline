import re


class APIUtils:
    """
    Class for API utilities
    """

    @staticmethod
    def isCorrectURL(url: str) -> bool:
        """
        Checks if the given URL is valid.

        Parameters
        ----------
        `url` : `str`
            The URL to be checked

        Returns
        -------
        `bool`
            `True` if the URL is valid, `False` otherwise
        """
        import validators

        return bool(validators.url(url))

    @staticmethod
    def extractRecordIdFromURL(url: str) -> str | None:
        """
        Extract the record ID from a URL.

        Parameters
        ----------
        `url` : `str`
            The URL

        Raises
        ------
        `ValueError`
            If the URL is not valid

        Returns
        -------
        `str | None`
            The record ID
        """
        if APIUtils.isCorrectURL(url):
            match = re.search(r"record/([a-zA-Z0-9]+)", url)
            if match:
                return match.group(1)
            return None
        else:
            raise ValueError(f"'{url}' is not a valid URL")
            return None

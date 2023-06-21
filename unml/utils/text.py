from typing import List

import fitz

from unml.utils.misc import log


class TextUtils:
    """
    Utility class for text related tasks.
    """

    @staticmethod
    def extractTextFromPDF(path: str, verbose: bool = False) -> str:
        """
        Extract text from a PDF file.

        Parameters
        ----------
        `path` : `str`
            The path to the PDF file
        `verbose` : `bool`
            The verbose argument. Defaults to `False`.

        Returns
        -------
        `str`
            The text from the PDF file
        """
        log("Extracting text from PDF...", level="info", verbose=verbose)

        doc = fitz.open(path)
        text = [page.get_text() for page in doc]

        return "\n".join(text)

    @staticmethod
    def extractTextFromFile(path: str, verbose: bool = False) -> str:
        """
        Extract text from a file.

        Parameters
        ----------
        `path` : `str`
            The path to the file
        `verbose` : `bool`
            The verbose argument. Defaults to `False`.

        Returns
        -------
        `str`
            The text from the file
        """
        log(f"Extracting text from '{path}'...", level="info", verbose=verbose)

        if path.lower().endswith(".pdf"):
            text = TextUtils.extractTextFromPDF(path=path, verbose=verbose)
        else:
            with open(path, "r", encoding="utf-8") as f:
                text = f.read()

        return text

    @staticmethod
    def cleanText(text: str) -> str:
        """
        Function to clean text before summarization. Removes newlines, extra spaces,
        and other stuff.

        Parameters
        ----------
        `text` : `str`
            The text to be cleaned

        Returns
        -------
        `str`
            The cleaned text
        """
        import re

        text = re.sub(r"\n", " ", text)
        text = re.sub(r"\s+", " ", text)
        text = text.replace(" .", ".")

        return text

    @staticmethod
    def isEndOfSentence(token: str) -> bool:
        """
        Detect if a token is the end of a sentence

        Parameters
        ----------
        `token` : `str`
            The token to be checked

        Returns
        -------
        `bool`
            True if the token is the end of a sentence, False otherwise
        """
        return token in {".", "!", "?"}

    @staticmethod
    def isSentenceValid(sentence: List[str]) -> bool:
        """
        Check if a sentence is valid or not

        Parameters
        ----------
        `sentence` : `List[str]`
            The sentence to be checked

        Returns
        -------
        `bool`
            True if the sentence is valid, False otherwise
        """
        if len(sentence) <= 1:
            return False

        return True

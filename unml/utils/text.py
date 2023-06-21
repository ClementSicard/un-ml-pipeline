import fitz

from unml.utils.misc import log


class TextUtils:
    """
    Utility class for text related tasks.
    """

    @staticmethod
    def extractTextFromPDF(path: str) -> str:
        """
        Extract text from a PDF file.

        Parameters
        ----------
        `path` : `str`
            The path to the PDF file

        Returns
        -------
        `str`
            The text from the PDF file
        """
        log("Extracting text from PDF...", level="info", verbose=True)

        doc = fitz.open(path)
        text = [page.get_text() for page in doc]

        return "\n".join(text)

    @staticmethod
    def extractTextFromFile(path: str) -> str:
        """
        Extract text from a file.

        Parameters
        ----------
        `path` : `str`
            The path to the file

        Returns
        -------
        `str`
            The text from the file
        """
        log(f"Extracting text from '{path}'...", level="info", verbose=True)

        if path.lower().endswith(".pdf"):
            text = TextUtils.extractTextFromPDF(path=path)
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

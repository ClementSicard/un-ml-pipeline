import os
from typing import Optional

import fitz
from loguru import logger
from requests import get

from unml.utils.consts import DOWNLOADS_FOLDER


class TextUtils:
    """
    Utility class for text related tasks.
    """

    @staticmethod
    def download_document(url: str, output: Optional[str] = None) -> str:
        """
        Download a document from a given URL.

        Parameters
        ----------
        `url` : `str`
            The URL of the document
        `output` : `Optional[str]`, optional
            Output destination, by default None

        Returns
        -------
        `str`
            The path to the downloaded document
        """
        logger.info(f"Downloading document from {url}...")

        if output is None:
            file_name = url.split("/")[-1]
            os.makedirs(DOWNLOADS_FOLDER, exist_ok=True)
            output = os.path.join(DOWNLOADS_FOLDER, file_name)

        with open(output, "wb") as f:
            f.write(get(url).content)

        logger.success(f"Document downloaded to {output}!")

        return output

    @staticmethod
    def extract_text_from_pdf(path: str) -> str:
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
        logger.info("Extracting text from PDF...")

        doc = fitz.open(path)
        text = [page.get_text() for page in doc]

        return "\n".join(text)

    @staticmethod
    def extract_text_from_file(path: str) -> str:
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
        logger.info(f"Extracting text from {path}...")

        if path.lower().endswith(".pdf"):
            text = TextUtils.extract_text_from_pdf(path=path)
        else:
            with open(path, "r", encoding="utf-8") as f:
                text = f.read()

        return text

    @staticmethod
    def get_document_text(url: str) -> str:
        """
        Get the text from a document at a given URL.

        Parameters
        ----------
        `url` : `str`
            The URL of the document

        Returns
        -------
        `str`
            The text from the document
        """
        outputPath = TextUtils.download_document(url=url)
        raw_text = TextUtils.extract_text_from_file(path=outputPath)

        return TextUtils.clean_text(text=raw_text)

    @staticmethod
    def clean_text(text: str) -> str:
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

        return text

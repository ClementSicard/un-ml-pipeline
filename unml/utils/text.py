import os
from typing import Optional

import fitz
from loguru import logger
from requests import get

from unml.utils.consts import DOWNLOADS_FOLDER


def downloadDocument(url: str, output: Optional[str] = None) -> str:
    logger.info(f"Downloading document from {url}...")

    if output is None:
        fileName = url.split("/")[-1]
        os.makedirs(DOWNLOADS_FOLDER, exist_ok=True)
        output = os.path.join(DOWNLOADS_FOLDER, fileName)

    with open(output, "wb") as f:
        f.write(get(url).content)

    logger.success(f"Document downloaded to {output}!")

    return output


def extractTextFromPDF(path: str) -> str:
    logger.info("Extracting text from PDF...")

    doc = fitz.open(path)
    text = [page.get_text() for page in doc]

    return "\n".join(text)


def extractTextFromFile(path: str) -> str:
    logger.info(f"Extracting text from {path}...")

    if path.lower().endswith(".pdf"):
        text = extractTextFromPDF(path=path)
    else:
        with open(path, "r", encoding="utf-8") as f:
            text = f.read()

    return text


def getDocumentText(url: str) -> str:
    outputPath = downloadDocument(url=url)
    text = extractTextFromFile(path=outputPath)

    return text

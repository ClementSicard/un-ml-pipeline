import re
from typing import List, Optional

import fitz
from transformers import PreTrainedTokenizer

from unml.utils.consts.countries import COUNTRIES
from unml.utils.consts.un_bodies import UN_BODIES
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
        log(f"Extracting text from PDF '{path}'...", level="info", verbose=verbose)
        doc = fitz.open(path)
        text = []
        for page in doc:
            text.append(page.get_text())

        extractedText = "\n".join(text)

        return extractedText

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

        # Replace new lines with spaces
        text = re.sub(r"\n", " ", text)

        # Harmonize spacing
        text = re.sub(r"\s+", " ", text)

        # Remove sequences of long dots
        text = re.sub(r"\.{4,}", " ", text)

        # Remove spaces before punctuation
        text = text.replace(" .", ".")

        return text.strip()

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

    @staticmethod
    def chunkTokens(
        tokens: List[str],
        tokenizer: PreTrainedTokenizer,
    ) -> List[str]:
        """
        Chunk a list of tokens into smaller chunks.

        Parameters
        ----------
        `tokens` : `List[str]`
            Full list of tokens to be chunked into multiple smaller chunks
        `tokenizer` : `PreTrainedTokenizer`
            The tokenizer to be used

        Returns
        -------
        `List[str]`
            List of chunks
        """
        chunks: List[str] = []
        currentChunk: List[str] = []
        currentSentence: List[str] = []

        maxChunkSize = tokenizer.model_max_length - 10

        for token in tokens:
            currentSentence += [token]
            isLast = token == tokens[-1]

            # If the token is the end of a sentence or the last token
            if TextUtils.isEndOfSentence(token) or isLast:
                # If the current chunk is not full, add the current sentence to it
                if len(currentChunk) + len(currentSentence) <= maxChunkSize:
                    if TextUtils.isSentenceValid(currentSentence):
                        currentChunk.extend(currentSentence)
                    currentSentence = []
                # Otherwise, save the chunk and start a new one with the current sentence
                else:
                    decodedChunk = tokenizer.convert_tokens_to_string(currentChunk)
                    chunks.append(decodedChunk)
                    currentChunk = currentSentence.copy()
                    currentSentence = []

        # For the last chunk, add it to the list of chunks
        decodedChunk = tokenizer.convert_tokens_to_string(currentChunk)
        chunks.append(decodedChunk)

        return chunks

    @staticmethod
    def isInvalidEntity(
        entity: str,
    ) -> bool:
        """
        Check if an entity is invalid.

        Parameters
        ----------
        `entity` : `str`
            The entity to be checked

        Returns
        -------
        `bool`
            True if the entity is invalid, False otherwise
        """
        invalid = False

        # Check if the entity is a single character
        invalid |= len(entity) == 1

        # Check if the entity is only numeric
        invalid |= entity.isnumeric()

        return invalid

    @staticmethod
    def getInitials(entity: str) -> str:
        """
        Get the initials of an entity.

        Parameters
        ----------
        `entity` : `str`
            The entity

        Returns
        -------
        `str`
            The initials of the entity
        """

        initials = "".join([w[0] for w in entity.split() if w[0].isupper()])

        return initials

    @staticmethod
    def replaceIfNotNull(
        string: Optional[str], pattern: str, replacement: str
    ) -> Optional[str]:
        """
        Replace a pattern in a string if the string is not None.

        Parameters
        ----------
        `string` : `Optional[str]`
            The string to be checked
        `pattern` : `str`
            The pattern to be replaced
        `replacement` : `str`
            The pattern to replace by

        Returns
        -------
        `str`
            The string with the pattern replaced or `None` if the string is `None`
        """
        if string is not None:
            string = string.replace(pattern, replacement)

        return string

    @staticmethod
    def extractCountries(text: str) -> List[str]:
        """
        Extract countries from a text.

        Parameters
        ----------
        `text` : `str`
            The text to be checked

        Returns
        -------
        `List[str]`
            Extracted countries from the text
        """
        countries = set()
        pattern = r"\b(" + "|".join(COUNTRIES) + r")\b"

        results = re.findall(pattern, text)
        for result in results:
            result = result[0]
            countries.add(result)

        return sorted(list(countries))

    @staticmethod
    def extractUNBodies(text: str) -> List[str]:
        """
        Extract UN Bodies from a text.

        Parameters
        ----------
        `text` : `str`
            The text to be checked

        Returns
        -------
        `List[str]`
            Extracted UN bodies from the text
        """
        countries = set()
        pattern = r"\b(" + "|".join(UN_BODIES) + r")\b"

        results = re.findall(pattern, text)
        for result in results:
            result = result[0]
            countries.add(result)

        return sorted(list(countries))

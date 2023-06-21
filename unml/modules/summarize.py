"""
This module contains the general `Summarizer` class, to summarize a text.
"""

from typing import List

from unml.models.summarize.DistilBART import DistillBART
from unml.utils.consts import SummarizationConsts
from unml.utils.misc import log
from unml.utils.text import TextUtils


class Summarizer:
    """
    This class represents a general object to summarize text.
    """

    def __init__(
        self,
        model: str = SummarizationConsts.DEFAULT_SUMMARIZATION_MODEL,
    ) -> None:
        match model:
            case "DistillBART":
                self.summarizer = DistillBART()
            case _:
                self.summarizer = DistillBART()

        self.maxChunkSize = self.summarizer.model.tokenizer.model_max_length
        self.tokenizer = self.summarizer.model.tokenizer

    def summarize(
        self,
        text: str,
        minLength: int = SummarizationConsts.SUMMARY_MIN_LENGTH,
        maxLength: int = SummarizationConsts.SUMMARY_MAX_LENGTH,
        doSample: bool = False,
        verbose: bool = False,
    ) -> str:
        """
        Summarize a text using the `model` attribute of the `Summarizer` class.
        Inspired by OpenAI's blog post(https://openai.com/research/summarizing-books)
        for long documents.

        Parameters
        ----------
        `text` : `str`
            The text to be summarized
        `minLength` : `int`, optional
            Minimum length of the summary, by default `SUMMARY_MIN_LENGTH`
        `maxLength` : `int`, optional
            Maximum length of the summary, by default `SUMMARY_MAX_LENGTH`
        `doSample` : `bool`, optional
            To do sample or not, by default False
        `verbose` : `bool`, optional
            Verbose argument, by default False

        Returns
        -------
        `str`
            The summarized text
        """
        log("Summarizing document...", verbose=verbose, level="info")

        # 1. Extract tokens from text
        tokens = self.tokenizer.tokenize(text)

        log(f"Number of tokens: {len(tokens)}", verbose=verbose, level="info")

        # If the number of tokens is less than the maximum chunk size,
        # summarize the text directly
        if len(tokens) <= self.maxChunkSize:
            result = self.summarizer.summarize(
                text=text,
                min_length=minLength,
                max_length=maxLength,
                do_sample=doSample,
            )

        # Otherwise, chunk the tokens and summarize each chunk, and recursively
        # summarize the result(s) until the result is less than the maximum chunk size
        else:
            inputSize = len(tokens)

            while inputSize > self.maxChunkSize:
                log(f"Input size: {inputSize}", verbose=verbose, level="debug")
                # 2. Chunk the tokens
                chunks = self.chunkTokens(tokens)

                log(f"Number of chunks: {len(chunks)}", verbose=verbose, level="debug")

                # 3. Summarize each chunk
                summaries = []
                for chunk in chunks:
                    summary = self.summarizer.summarize(
                        text=chunk,
                        min_length=minLength,
                        max_length=maxLength,
                        do_sample=doSample,
                    )
                    summaries.append(summary)

                # 4. Join the summaries
                result = "".join(summaries)
                inputSize = len(self.tokenizer.tokenize(result))

        result = TextUtils.cleanText(text=result)

        log(
            f"Done! Result is {len(result)} characters long",
            verbose=verbose,
            level="success",
        )
        return result

    def chunkTokens(self, tokens: List[str]) -> List[str]:
        """
        Chunk a list of tokens into smaller chunks.

        Parameters
        ----------
        `tokens` : `List[str]`
            Full list of tokens to be chunked into multiple smaller chunks

        Returns
        -------
        `List[str]`
            List of chunks
        """
        chunks: List[str] = []
        currentChunk: List[str] = []
        currentSentence: List[str] = []

        for token in tokens:
            currentSentence += [token]
            isLast = token == tokens[-1]

            # If the token is the end of a sentence or the last token
            if TextUtils.isEndOfSentence(token) or isLast:
                # If the current chunk is not full, add the current sentence to it
                if len(currentChunk) + len(currentSentence) <= self.maxChunkSize:
                    if TextUtils.isSentenceValid(currentSentence):
                        currentChunk.extend(currentSentence)
                    currentSentence = []
                # Otherwise, save the chunk and start a new one with the current sentence
                else:
                    decoded_chunk = self.tokenizer.convert_tokens_to_string(
                        currentChunk
                    )
                    chunks.append(decoded_chunk)
                    currentChunk = currentSentence.copy()
                    currentSentence = []

        # For the last chunk, add it to the list of chunks
        decoded_chunk = self.tokenizer.convert_tokens_to_string(currentChunk)
        chunks.append(decoded_chunk)

        return chunks

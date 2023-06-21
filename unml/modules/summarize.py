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

        self.max_chunk_size = self.summarizer.model.tokenizer.model_max_length
        self.tokenizer = self.summarizer.model.tokenizer

    def summarize(
        self,
        text: str,
        min_length: int = SummarizationConsts.SUMMARY_MIN_LENGTH,
        max_length: int = SummarizationConsts.SUMMARY_MAX_LENGTH,
        do_sample: bool = False,
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
        `min_length` : `int`, optional
            Minimum length of the summary, by default `SUMMARY_MIN_LENGTH`
        `max_length` : `int`, optional
            Maximum length of the summary, by default `SUMMARY_MAX_LENGTH`
        `do_sample` : `bool`, optional
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

        if len(tokens) <= self.max_chunk_size:
            result = self.summarizer.summarize(
                text=text,
                min_length=min_length,
                max_length=max_length,
                do_sample=do_sample,
            )

        else:
            input_size = len(tokens)

            while input_size > self.max_chunk_size:
                log(f"Input size: {input_size}", verbose=verbose, level="debug")
                # 2. Chunk the tokens
                chunks = self.chunk_tokens(tokens)

                log(f"Number of chunks: {len(chunks)}", verbose=verbose, level="debug")

                # 3. Summarize each chunk
                summaries = []
                for chunk in chunks:
                    summary = self.summarizer.summarize(
                        text=chunk,
                        min_length=min_length,
                        max_length=max_length,
                        do_sample=do_sample,
                    )
                    summaries.append(summary)

                # 4. Join the summaries
                result = "".join(summaries)
                input_size = len(self.tokenizer.tokenize(result))

        result = TextUtils.cleanText(text=result)

        log(
            f"Done! Result is {len(result)} characters long",
            verbose=verbose,
            level="success",
        )
        return result

    def chunk_tokens(self, tokens: List[str]) -> List[str]:
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
        current_chunk: List[str] = []
        current_sentence: List[str] = []

        for token in tokens:
            current_sentence += [token]
            is_last = token == tokens[-1]

            # If the token is the end of a sentence or the last token
            if self.is_eos(token) or is_last:
                # If the current chunk is not full, add the current sentence to it
                if len(current_chunk) + len(current_sentence) <= self.max_chunk_size:
                    if self.is_sentence_valid(current_sentence):
                        current_chunk.extend(current_sentence)
                    current_sentence = []
                # Otherwise, save the chunk and start a new one with the current sentence
                else:
                    decoded_chunk = self.tokenizer.convert_tokens_to_string(
                        current_chunk
                    )
                    chunks.append(decoded_chunk)
                    current_chunk = current_sentence.copy()
                    current_sentence = []

        # For the last chunk, add it to the list of chunks
        decoded_chunk = self.tokenizer.convert_tokens_to_string(current_chunk)
        chunks.append(decoded_chunk)

        return chunks

    def is_eos(self, token: str) -> bool:
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

    def is_sentence_valid(self, sentence: List[str]) -> bool:
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

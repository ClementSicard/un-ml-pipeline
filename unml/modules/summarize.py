"""
This module contains the general `Summarizer` class, to summarize a text.
"""


from unml.models.summarize.DistilBARTCNN import DistilBARTCNN
from unml.models.summarize.DistilBARTXSUM import DistilBARTXSUM
from unml.models.summarize.DistilPegasusCNN import DistilPegasusCNN
from unml.models.summarize.LED import LED
from unml.models.summarize.LongT5 import LongT5
from unml.utils.consts.summarize import SummarizationConsts
from unml.utils.misc import log
from unml.utils.text import TextUtils


class Summarizer:
    """
    This class represents a general object to summarize text.
    """

    summarizer: DistilBARTCNN | DistilBARTXSUM | DistilPegasusCNN | LED | LongT5

    def __init__(
        self,
        model: str = SummarizationConsts.DEFAULT_SUMMARIZATION_MODEL,
    ) -> None:
        parsedModel = SummarizationConsts.ARGS_MAP[model]
        match parsedModel:
            case "DistilBARTCNN":
                self.summarizer = DistilBARTCNN()
            case "DistilBARTXSUM":
                self.summarizer = DistilBARTXSUM()
            case "DistilPegasusCNN":
                self.summarizer = DistilPegasusCNN()
            case "LED":
                self.summarizer = LED()
            case "LongT5":
                self.summarizer = LongT5()
            case _:
                self.summarizer = LED()

        self.tokenizer = self.summarizer.model.tokenizer
        self.maxChunkSize = self.tokenizer.model_max_length - 10

        log(
            f"Summarizer {parsedModel} instantiated! Max chunk size: {self.maxChunkSize:,}",
            verbose=True,
            level="success",
        )

    def summarize(
        self,
        text: str,
        minLength: int = SummarizationConsts.SUMMARY_MIN_LENGTH,
        maxLength: int = SummarizationConsts.SUMMARY_MAX_TOKEN_LENGTH,
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
            Maximum length of the summary, by default `SUMMARY_MAX_TOKEN_LENGTH`
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
        nTokens = len(tokens)

        log(f"Number of tokens: {len(tokens):,}", verbose=verbose, level="info")

        # If the number of tokens is less than the maximum chunk size,
        # summarize the text directly
        if len(tokens) <= self.maxChunkSize:
            result = self.summarizer.summarize(
                text=text,
                minLength=minLength,
                maxLength=maxLength,
                doSample=doSample,
            )

        # Otherwise, chunk the tokens and summarize each chunk, and recursively
        # summarize the result(s) until the result is less than the maximum chunk size
        else:
            resultTokens = tokens.copy()
            while nTokens > self.maxChunkSize:
                log(f"Input size: {nTokens:,}", verbose=verbose, level="debug")
                # 2. Chunk the tokens
                chunks = TextUtils.chunkTokens(
                    tokens=resultTokens,
                    tokenizer=self.tokenizer,
                )

                log(
                    f"Number of chunks: {len(chunks):,}", verbose=verbose, level="debug"
                )

                # 3. Summarize each chunk
                summaries = []
                for chunk in chunks:
                    summary = self.summarizer.summarize(
                        text=chunk,
                        minLength=minLength,
                        maxLength=maxLength,
                        doSample=doSample,
                    )
                    summaries.append(summary)

                # 4. Join the summaries
                result = TextUtils.cleanText(text="".join(summaries))
                resultTokens = self.tokenizer.tokenize(result)
                nTokens = len(resultTokens)

                log(
                    f"Number of tokens of the result: {len(resultTokens):,}",
                    verbose=verbose,
                    level="debug",
                )

        log(f"Summary: {result}", verbose=verbose)
        log(
            f"Done! Summary is {len(result):,} characters long",
            verbose=verbose,
            level="success",
        )

        return result

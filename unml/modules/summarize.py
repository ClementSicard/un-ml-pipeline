"""
This module contains the general `Summarizer` class, to summarize a text.
"""

from unml.models.summarize.DistilBART import DistillBART
from unml.utils.consts import (
    DEFAULT_SUMMARIZATION_MODEL,
    SUMMARY_MAX_LENGTH,
    SUMMARY_MIN_LENGTH,
)
from unml.utils.misc import log


class Summarizer:
    """
    This class represent an general object to summarize text.
    """

    MODELS = {"distilbart"}

    def __init__(self, model: str = DEFAULT_SUMMARIZATION_MODEL) -> None:
        match model:
            case "distilbart":
                self.model = DistillBART()
            case _:
                self.model = DistillBART()

    def summarize(
        self,
        text: str,
        min_length: int = SUMMARY_MIN_LENGTH,
        max_length: int = SUMMARY_MAX_LENGTH,
        do_sample: bool = False,
        verbose: bool = False,
    ) -> str:
        """
        Summarize a text using the `model` attribute of the `Summarizer` class

        Parameters
        ----------
        `text` : `str`
            The text to be summarized
        `min_length` : `int`, optional
            Minimum length of the summary, by default SUMMARY_MIN_LENGTH
        `max_length` : `int`, optional
            Maximum length of the summary, by default SUMMARY_MAX_LENGTH
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
        result = self.model.summarize(
            text=text,
            min_length=min_length,
            max_length=max_length,
            do_sample=do_sample,
        )
        log("Done!", verbose=verbose, level="success")

        return result

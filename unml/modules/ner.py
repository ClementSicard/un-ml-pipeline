from typing import Dict, List

from unml.models.ner.RoBERTa import RoBERTa
from unml.utils.consts import NERConsts
from unml.utils.misc import log


class NamedEntityRecognizer:
    """
    This class represents a general object to recognize named entities in text.
    """

    def __init__(
        self,
        model: str = NERConsts.DEFAULT_NER_MODEL,
    ) -> None:
        match model:
            case "RoBERTa":
                self.nerExtractor = RoBERTa()
            case _:
                self.nerExtractor = RoBERTa()

    def recognize(self, text: str, verbose: bool = False) -> List[Dict[str, str | int]]:
        """
        Recognize named entities in a text.

        Parameters
        ----------
        `text` : `str`
            The text from which we need to extract named entities

        Returns
        -------
        `List[Dict[str, str | int]]`
            The list of named entities in the text in the format:
            ```
            [
                {
                    "entity_group": "MISC",
                    "score": 0.99381506,
                    "word": "WFP",
                    "start": 0,
                    "end": 5,
                },
                ...
            ]
            ```
        """
        results = self.nerExtractor.recognize(text)

        log(
            f"Named entities: {sorted([r['word'] for r in results])}",
            verbose=verbose,
            level="debug",
        )

        return results

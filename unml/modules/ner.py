from typing import Any, Dict, List, Tuple

from unml.models.ner.RoBERTa import RoBERTa
from unml.utils.consts.ner import NERConsts
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

    def recognize(
        self, text: str, verbose: bool = False
    ) -> Tuple[List[str], List[Dict[str, Any]]]:
        """
        Recognize named entities in a text.

        Parameters
        ----------
        `text` : `str`
            The text from which we need to extract named entities

        Returns
        -------
        `Tuple[List[str], List[Dict[str, Any]]]`
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

        for result in results:
            result["score"] = float(f'{result["score"]:.3f}')

        entities = sorted(list({str(r["word"]).strip() for r in results}))

        log(
            f"Named entities: {entities[:10] if len(entities) > 10 else entities}",
            verbose=verbose,
            level="debug",
        )

        return entities, results

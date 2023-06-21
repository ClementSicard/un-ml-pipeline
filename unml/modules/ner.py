from typing import Any, Dict, List

from unml.models.ner.roberta import RoBERTa
from unml.utils.consts import NERConsts


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

    def predict(self, text: str) -> List[Dict[str, Any]]:
        """
        Recognize named entities in a text.

        Parameters
        ----------
        `text` : `str`
            The text from which we need to extract named entities

        Returns
        -------
        `List[Dict[str, Any]]`
            The list of named entities in the text

        """
        doc = self.nerExtractor.model(text)
        return [
            {
                "text": ent.text,
                "label": ent.label_,
                "start_char": ent.start_char,
                "end_char": ent.end_char,
            }
            for ent in doc.ents
        ]

from typing import Dict, List

from unml.models.model import Model


class RoBERTa(Model):
    """
    Class for RoBERTa (Liu et al., 2019) model
    """

    MODEL_NAME = "Jean-Baptiste/roberta-large-ner-english"

    def __init__(self, modelName: str = MODEL_NAME) -> None:
        super().__init__(modelName=modelName, task="ner", aggregation_strategy="simple")

    def recognize(self, text: str) -> List[Dict[str, str | int]]:
        """
        See doc for `NamedEntityRecognizer` class
        """
        result: List[Dict[str, str | int]] = self.model(text)

        return result

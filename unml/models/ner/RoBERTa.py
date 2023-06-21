from unml.models.model import Model
from unml.utils.misc import log


class RoBERTa(Model):
    """
    Class for RoBERTa (Liu et al., 2019) model
    """

    MODEL_NAME = "Jean-Baptiste/roberta-large-ner-english"

    def __init__(self, modelName: str = MODEL_NAME) -> None:
        super().__init__(modelName=modelName, task="ner")

    def predict(self, text: str) -> str:
        """
        See doc for `NamedEntityRecognizer` class
        """

        output = self.model(text)

        log(f"Predicted named entities: {output}", level="info", verbose=True)

        return str(output)

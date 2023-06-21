from unml.models.model import Model


class RoBERTa(Model):
    """
    Class for RoBERTa (Liu et al., 2019) model
    """

    MODEL_NAME = "Jean-Baptiste/roberta-large-ner-english"

    def __init__(self, model_name: str = MODEL_NAME) -> None:
        super().__init__(modelName=model_name, task="ner")

    def predict(self, text: str) -> str:
        """
        See doc for `NamedEntityRecognizer` class
        """

        output = self.model(text)

        return str(output)

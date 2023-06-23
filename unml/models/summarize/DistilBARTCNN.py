from unml.models.model import Model
from unml.utils.consts.summarize import SummarizationConsts


class DistilBARTCNN(Model):
    """
    Class for DistilBART (Sanh et al., 2019) model
    """

    MODEL_NAME = "sshleifer/distilbart-cnn-12-6"

    def __init__(self, modelName: str = MODEL_NAME) -> None:
        super().__init__(modelName=modelName, task="summarization")

    def summarize(
        self,
        text: str,
        minLength: int = SummarizationConsts.SUMMARY_MIN_LENGTH,
        maxLength: int = SummarizationConsts.SUMMARY_MAX_TOKEN_LENGTH,
        doSample: bool = False,
    ) -> str:
        """
        See doc for `Summarizer` class
        """
        output = self.model(
            text,
            min_length=minLength,
            max_length=maxLength,
            do_sample=doSample,
        )

        return str(output[0]["summary_text"])

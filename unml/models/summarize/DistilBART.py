from unml.models.model import Model
from unml.utils.consts import SummarizationConsts


class DistillBART(Model):
    """
    Class for DistillBART (Sanh et al., 2019) model
    """

    MODEL_NAME = "sshleifer/distilbart-cnn-12-6"

    def __init__(self, model_name: str = MODEL_NAME) -> None:
        super().__init__(modelName=model_name, task="summarization")

    def summarize(
        self,
        text: str,
        min_length: int = SummarizationConsts.SUMMARY_MIN_LENGTH,
        max_length: int = SummarizationConsts.SUMMARY_MAX_LENGTH,
        do_sample: bool = False,
    ) -> str:
        """
        See doc for `Summarizer` class
        """
        output = self.model(
            text,
            min_length=min_length,
            max_length=max_length,
            do_sample=do_sample,
        )

        return str(output[0]["summary_text"])

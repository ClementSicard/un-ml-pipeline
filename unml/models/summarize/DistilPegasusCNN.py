from unml.models.model import Model
from unml.utils.consts.summarize import SummarizationConsts


class DistilPegasusCNN(Model):
    """
    Class for distilled Pegasus (Liu et al., 2020) model
    """

    MODEL_NAME = "sshleifer/distill-pegasus-cnn-16-4"

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
            no_repeat_ngram_size=3,
            encoder_no_repeat_ngram_size=3,
            repetition_penalty=3.5,
            num_beams=4,
            early_stopping=True,
        )

        return str(output[0]["summary_text"])

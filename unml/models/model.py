from transformers import Pipeline, pipeline

from unml.utils.consts import ML_TASKS


class Model:
    """
    Generic class for a ML model
    """

    model_name: str
    task: str
    model: Pipeline

    def __init__(
        self,
        model_name: str,
        task: str,
    ) -> None:
        self.model_name = model_name

        assert task in ML_TASKS, f"Invalid task: {task}. Must be one of {ML_TASKS}"

        self.task = task
        self.model = pipeline(task, model=model_name)

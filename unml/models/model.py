from typing import Any

from transformers import Pipeline, pipeline

from unml.utils.consts.model import ModelConsts


class Model:
    """
    Generic class for a ML model
    """

    modelName: str
    task: str
    model: Pipeline

    def __init__(
        self,
        modelName: str,
        task: str,
        **kwargs: Any,
    ) -> None:
        self.modelName = modelName

        assert (
            task in ModelConsts.ML_TASKS
        ), f"Invalid task: {task}. Must be one of {ModelConsts.ML_TASKS}"

        self.task = task
        self.model = pipeline(task, model=modelName, **kwargs)

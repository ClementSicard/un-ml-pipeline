from typing import Any, Dict, Optional

from transformers import Pipeline, pipeline

from unml.utils.consts import ML_TASKS


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
        **kwargs: Optional[Dict[str, Any]],
    ) -> None:
        self.modelName = modelName

        assert task in ML_TASKS, f"Invalid task: {task}. Must be one of {ML_TASKS}"

        self.task = task
        self.model = pipeline(task, model=modelName, **kwargs)

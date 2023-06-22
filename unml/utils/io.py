import os
from typing import Any, Dict, Optional

from unml.utils.consts.io import IOConsts
from unml.utils.misc import log


class IOUtils:
    """
    Utility class for IO related tasks.
    """

    @staticmethod
    def saveFile(fileName: str, content: str | bytes | Dict[str, Any]) -> Optional[str]:
        """
        Save a the contents of a file to a given path.

        Parameters
        ----------
        `fileName` : `str`
            The name of the file, in the format `name.extension`. The file will be
            saved in the `DOWNLOADS_FOLDER` directory.
        `content` : `str | bytes`
            The contents of the file, either as a string or as bytes

        Returns
        -------
        `Optional[str]`
            The path to the saved file, or `None` if an error occurred
        """
        os.makedirs(IOConsts.DOWNLOADS_FOLDER, exist_ok=True)
        output = os.path.join(IOConsts.DOWNLOADS_FOLDER, fileName)

        if os.path.exists(output):
            log(
                f'File "{output}" already exists, skipping...',
                level="warning",
                verbose=True,
            )
            return output

        try:
            with open(output, "wb" if isinstance(content, bytes) else "w") as f:
                f.write(content)

            return output
        except Exception as e:
            log(
                f'Error while saving file "{fileName}": {e}',
                level="error",
                verbose=True,
            )
            exit()

    @staticmethod
    def saveResults(results: Dict[str, Any]) -> None:
        """
        Save the results of a task to a file.

        Parameters
        ----------
        `results` : `Dict[str, Any]`
            The results of the task
        `verbose` : `bool`
            The verbose argument. Defaults to `False`.
        """
        log("Saving results...", level="info", verbose=True)

        fileName = f"{results['task']}.json"
        output = IOUtils.saveFile(fileName=fileName, content=results)

        if output is not None:
            log(f"Results saved to {output}!", level="success", verbose=True)

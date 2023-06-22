import json
import os
from typing import Any, Dict, Optional

from unml.utils.consts.io import IOConsts
from unml.utils.misc import log


class IOUtils:
    """
    Utility class for IO related tasks.
    """

    @staticmethod
    def saveFileToDownloads(
        fileName: str,
        content: str | bytes | Dict[str, Any],
    ) -> Optional[str]:
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

        return IOUtils.saveFile(filePath=output, content=content)

    @staticmethod
    def saveFile(
        filePath: str,
        content: str | bytes | Dict[Any, Any],
        overwrite: bool = False,
    ) -> Optional[str]:
        """
        Save a the contents of a file to a given path.

        Parameters
        ----------
        `filePath` : `str`
            The path to the file
        `content` : `str | bytes`
            The contents of the file, either as a string or as bytes

        Returns
        -------
        `Optional[str]`
            The path to the saved file, or `None` if an error occurred
        """

        if os.path.exists(filePath) and not overwrite:
            log(
                f'File "{filePath}" already exists, skipping...',
                level="warning",
                verbose=True,
            )
            return filePath

        try:
            log(f"Type of content: {type(content)}", verbose=True)
            with open(filePath, "wb" if isinstance(content, bytes) else "w") as f:
                if not isinstance(content, (dict, list)):
                    f.write(content)
                else:
                    json.dump(
                        content,
                        f,
                        ensure_ascii=False,
                        indent=4,
                    )

            return filePath
        except Exception as e:
            log(
                f'Error while saving file "{filePath}": {e}',
                level="error",
                verbose=True,
            )
            exit(1)

    @staticmethod
    def saveResults(results: Dict[str, Any], path: str) -> Optional[str]:
        """
        Save the results of a task to a file.

        Parameters
        ----------
        `results` : `Dict[str, Any]`
            The results of the task
        `path` : `str`
            The path to the output file

        Returns
        -------
        `Optional[str]`
            The path to the output file
        """
        log(f"Saving results to '{path}'...", level="info", verbose=True)

        output = IOUtils.saveFile(filePath=path, content=results, overwrite=True)

        if output is not None:
            log(f"Results saved to {output}!", level="success", verbose=True)

        return output

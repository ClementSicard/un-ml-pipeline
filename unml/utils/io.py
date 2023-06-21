import os

from unml.utils.consts import DOWNLOADS_FOLDER
from unml.utils.misc import log


class IOUtils:
    """
    Utility class for IO related tasks.
    """

    @staticmethod
    def saveFile(
        fileName: str, content: str | bytes, verbose: bool = False
    ) -> str | None:
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
        `str | None`
            The path to the saved file, or `None` if an error occurred
        """
        os.makedirs(DOWNLOADS_FOLDER, exist_ok=True)
        output = os.path.join(DOWNLOADS_FOLDER, fileName)

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

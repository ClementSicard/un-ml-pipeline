from pathlib import Path


class IOConsts:
    """
    IO constants
    """

    DOWNLOADS_FOLDER = Path.home() / ".unml" / "downloads"
    PROJECT_ROOT = Path(__file__).parent.parent.parent.parent

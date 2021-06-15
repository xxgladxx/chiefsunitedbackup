import logging

from redbot.core.data_manager import cog_data_path
from redbot.logging import RotatingFileHandler

from typing import Optional

__all__ = ["DisabledConsoleOutput", "init_logger", "close_logger"]


class DisabledConsoleOutput:
    """
    A context manager that disables parent handlers, including console output.

    This is useful if you need to log something that the parent already handle (like
    command errors with Red).

    .. admonition:: Example

        .. code-block:: python

            with DisabledConsoleOutput(log):
                log.error("Error in command {command.name}.")

    Parameters
    ----------
    log: logging.Logger
        The logger object.
    """

    def __init__(self, log: logging.Logger):
        self.log = log

    def __enter__(self):
        self.log.propagate = False

    def __exit__(self):
        self.log.propagate = True


def init_logger(log: logging.Logger, cog_name: str, package_name: Optional[str] = None):
    """
    Prepare the logger for laggron cogs.

    Parameters
    ----------
    log: logging.Logger
        The logger object.
    cog_name: str
        The CamelCase name of the cog, used for cog data path.
    package_name: Optional[str]
        The name of the package, used for file names. Defaults to the lowercase cog name.
    """
    if package_name is None:
        package_name = cog_name.lower()
    formatter = logging.Formatter(
        "[{asctime}] [{levelname}] {name}: {message}", datefmt="%Y-%m-%d %H:%M:%S", style="{"
    )
    # logging to a log file
    # file is automatically created by the module, if the parent foler exists
    cog_path = cog_data_path(raw_name=cog_name)
    if cog_path.exists():
        file_handler = RotatingFileHandler(
            stem=package_name,
            directory=cog_path,
            maxBytes=1_000_000,
            backupCount=8,
            encoding="utf-8",
        )
        file_handler.setLevel(logging.DEBUG)
        file_handler.setFormatter(formatter)
        log.addHandler(file_handler)


def close_logger(log: logging.Logger):
    for handler in log.handlers:
        handler.close()
    log.handlers = []

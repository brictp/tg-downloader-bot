from .delete_video import delete_file
from .logger import logger
from .log_context import LogContext
from .enums import MediaFormat
from .parser import get_params_from_message


def __getattr__(name):
    if name == "download_media":
        from .downloader import download_media
        return download_media
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")


__all__ = [
    "download_media",
    "delete_file",
    "logger",
    "LogContext",
    "MediaFormat",
    "get_params_from_message",
]
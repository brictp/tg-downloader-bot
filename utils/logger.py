import os
import sys

from loguru import logger


def _get_patcher():
    from utils.log_context import log_context_patcher
    return log_context_patcher


LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO").upper()
LOG_FORMAT = os.getenv("LOG_FORMAT", "pretty")

logger.remove()
logger.configure(patcher=_get_patcher())

if LOG_FORMAT == "json":
    logger.add(
        sys.stderr,
        level=LOG_LEVEL,
        serialize=True,
    )
else:
    logger.add(
        sys.stderr,
        level=LOG_LEVEL,
        format=(
            "<green>{time:HH:mm:ss}</green> | "
            "<level>{level:<7}</level> | "
            "<cyan>{message}</cyan>"
            "<dim>{extra}</dim>"
        ),
        colorize=True,
    )
import os
import sys

from loguru import logger

from config.settings import DEV_MODE, LOG_FILE


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

if DEV_MODE:
    LOG_FILE.parent.mkdir(parents=True, exist_ok=True)
    logger.add(
        LOG_FILE,
        level=LOG_LEVEL,
        format="{time:YYYY-MM-DD HH:mm:ss} | {level:<7} | {message} | {extra}",
        rotation="10 MB",
        retention="7 days",
        encoding="utf-8",
    )
    logger.info("File logging enabled (dev mode)", path=str(LOG_FILE))


class YtDlpLogBridge:
    def debug(self, msg):
        logger.debug(msg)

    def info(self, msg):
        logger.info(msg)

    def warning(self, msg):
        logger.warning(msg)

    def error(self, msg):
        logger.error(msg)
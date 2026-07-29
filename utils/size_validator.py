from yt_dlp import YoutubeDL

from utils import logger
from config.settings import MAX_FILE_SIZE_VIDEO, MAX_FILE_SIZE_AUDIO
from utils.enums import MediaFormat


def get_max_bytes(format_type: MediaFormat) -> int:
    if format_type == MediaFormat.MP3:
        return MAX_FILE_SIZE_AUDIO
    return MAX_FILE_SIZE_VIDEO


def validate_media_size(url: str, format_type: MediaFormat) -> tuple[bool, str | None]:
    from handlers.downlaod_config_factory import DownloadConfigFactory

    options = DownloadConfigFactory.get_config(format_type)
    options["download"] = False

    try:
        with YoutubeDL(options) as ydl:
            info = ydl.extract_info(url, download=False)
    except Exception as e:
        logger.exception("Failed to extract metadata for size validation", url=url)
        return True, None

    max_bytes = get_max_bytes(format_type)
    max_mb = max_bytes // (1024 * 1024)

    size = info.get("filesize")
    if size and size > max_bytes:
        return False, f"El archivo excede el límite de {max_mb}MB"

    size_approx = info.get("filesize_approx")
    if size_approx and size_approx > max_bytes:
        return False, f"El archivo excede el límite de {max_mb}MB"

    requested = info.get("requested_formats")
    if requested:
        total = sum(f.get("filesize") or f.get("filesize_approx") or 0 for f in requested)
        if total > max_bytes:
            return False, f"El archivo excede el límite de {max_mb}MB"

    logger.info("Media size validated", url=url, max_bytes=max_bytes)
    return True, None